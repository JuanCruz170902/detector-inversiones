"""Corrida diaria del detector.

Uso:
    python -m src.main                         # corrida completa (la que hace GitHub Actions)
    python -m src.main --monto 300000 --perfil riesgoso   # propuesta puntual, imprime en pantalla
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import traceback
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from . import fuentes as F
from . import metricas as M
from . import motor
from . import paper

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "data"


def cargar_config():
    perfiles = yaml.safe_load((RAIZ / "config" / "perfiles.yaml").read_text(encoding="utf-8"))
    universo = yaml.safe_load((RAIZ / "config" / "universo.yaml").read_text(encoding="utf-8"))
    return perfiles, universo


class Registro:
    """Guarda qué fuente funcionó y cuál falló, para mostrarlo en el informe."""

    def __init__(self):
        self.estado = {}

    def tomar(self, nombre, fn, *a):
        try:
            r = fn(*a)
            self.estado[nombre] = "ok"
            return r
        except Exception as e:  # noqa: BLE001
            self.estado[nombre] = f"error: {e}"[:200]
            traceback.print_exc()
            return None


def ultimo_por_casa(dolares: list[dict] | None) -> dict:
    out = {}
    for d in dolares or []:
        casa = d.get("casa")
        if casa and (casa not in out or d.get("fecha", "") > out[casa].get("fecha", "")):
            out[casa] = d
    return out


def armar_macro(reg: Registro, raw: dict) -> dict:
    macro = {}
    infl = raw.get("inflacion")
    if infl:
        infl = sorted(infl, key=lambda x: x["fecha"])
        macro["inflacion_mensual"] = float(infl[-1]["valor"])
        macro["inflacion_fecha"] = infl[-1]["fecha"]
        macro["inflacion_3m_prom"] = round(statistics.mean(float(x["valor"]) for x in infl[-3:]), 2)
    pf = raw.get("plazo_fijo")
    if pf:
        tnas = [float(x["tnaClientes"]) for x in pf if x.get("tnaClientes")]
        if tnas:
            tna = statistics.mean(tnas)
            macro["tna_plazo_fijo"] = round(tna * 100 if tna < 1.5 else tna, 2)
    if "tna_plazo_fijo" not in macro and raw.get("bcra"):
        # respaldo: TAMAR (tasa mayorista de plazo fijo) del BCRA
        for k in ("tamar", "badlar"):
            if k in raw["bcra"]:
                macro["tna_plazo_fijo"] = round(raw["bcra"][k]["valor"], 2)
                macro["tna_fuente"] = k.upper()
                break
    casas = ultimo_por_casa(raw.get("dolares"))
    if "oficial" in casas:
        macro["dolar_oficial"] = float(casas["oficial"]["venta"])
    if "bolsa" in casas:
        macro["dolar_mep"] = float(casas["bolsa"]["venta"])
    if "contadoconliqui" in casas:
        macro["dolar_ccl"] = float(casas["contadoconliqui"]["venta"])
    if "blue" in casas:
        macro["dolar_blue"] = float(casas["blue"]["venta"])
    if not macro.get("dolar_mep") and raw.get("mep"):
        marks = [float(x["mark"]) for x in raw["mep"] if x.get("mark")]
        if marks:
            macro["dolar_mep"] = statistics.median(marks)
    rp = raw.get("riesgo_pais")
    if rp:
        macro["riesgo_pais"] = float(rp["valor"])
    for k, v in (raw.get("bcra") or {}).items():
        macro[f"bcra_{k}"] = v["valor"]
    return macro


def correr(monto: float | None = None, solo_perfil: str | None = None, con_historia: bool = True,
           guardar: bool = True) -> dict:
    perfiles, universo = cargar_config()
    monto = monto or perfiles["monto_default"]
    reg = Registro()

    raw = {
        "inflacion": reg.tomar("argdatos_inflacion", F.inflacion),
        "plazo_fijo": reg.tomar("argdatos_plazo_fijo", F.plazo_fijo),
        "dolares": reg.tomar("argdatos_dolares", F.dolares),
        "riesgo_pais": reg.tomar("argdatos_riesgo_pais", F.riesgo_pais),
        "bonos_cer": reg.tomar("argdatos_bonos_cer", F.bonos_cer),
        "bcra": reg.tomar("bcra", F.bcra_principales),
        "mep": reg.tomar("data912_mep", F.mep),
    }
    paneles = {n: M.panel_a_df(reg.tomar(f"data912_{n}", F.panel, n) or []) for n in F.PANELES}
    macro = armar_macro(reg, raw)

    # ---- renta fija en pesos ----
    rf = M.renta_fija_pesos(paneles["bonos"], paneles["letras"], tuple(perfiles["horizonte_meses"]))
    cer_tir = None
    if raw["bonos_cer"]:
        cer_tir = pd.DataFrame(raw["bonos_cer"].get("bonos", []))
        if not cer_tir.empty:
            cer_tir = cer_tir.rename(columns={"tirPorcentaje": "tir"})
    rank_rf = motor.ranking_renta_fija(rf, cer_tir, tuple(perfiles["horizonte_meses"]))

    hd = paneles["bonos"]
    if not hd.empty:
        orden = {t: i for i, t in enumerate(universo["hard_dollar"])}
        hd = hd[hd["ticker"].isin(orden) & (hd["precio"] > 0)].copy()
        hd["orden"] = hd["ticker"].map(orden)
        hd = hd.sort_values("orden")

    # ---- renta variable: historia y métricas ----
    met = {"cedears_etf": {}, "cedears": {}, "acciones_arg": {}}
    if con_historia:
        for grupo, tipo in (("cedears_etf", "cedears"), ("cedears", "cedears"), ("acciones_arg", "stocks")):
            for t in universo[grupo]:
                barras = reg.tomar(f"hist_{t}", F.historia, tipo, t)
                met[grupo][t] = M.metricas_historia(barras) if barras else None
        # resumo el estado de las historias en una sola línea
        fallas = [k for k, v in reg.estado.items() if k.startswith("hist_") and v != "ok"]
        reg.estado = {k: v for k, v in reg.estado.items() if not k.startswith("hist_")}
        reg.estado["data912_historia"] = "ok" if not fallas else f"fallaron {len(fallas)}: {', '.join(f[5:] for f in fallas[:8])}"

    # ---- por perfil ----
    resultado = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "fuentes": reg.estado, "macro": macro, "perfiles": {}, "monto": monto}
    nombres = [solo_perfil] if solo_perfil else list(perfiles["perfiles"])
    for nombre in nombres:
        p = perfiles["perfiles"][nombre]
        sen = motor.senales_macro(macro, p)
        buckets = motor.ajustar_buckets(p, sen)
        filtros = p.get("filtros_renta_variable", {"solo_tendencia_alcista": True, "vol_max_anual": 0.35})
        cfg_s = perfiles["scoring_renta_variable"]
        rv = {
            "cedears_etf": motor.ranking_renta_variable(met["cedears_etf"], paneles["cedears"], cfg_s, filtros, M.score_renta_variable),
            "cedears": motor.ranking_renta_variable({**met["cedears_etf"], **met["cedears"]}, paneles["cedears"], cfg_s, filtros, M.score_renta_variable),
            "acciones_arg": motor.ranking_renta_variable(met["acciones_arg"], paneles["acciones"], cfg_s, filtros, M.score_renta_variable),
        }
        candidatos = {**rank_rf, "hard_dollar": hd, **rv}
        prop = motor.proponer(nombre, p, buckets, candidatos, monto, perfiles["broker"])
        resultado["perfiles"][nombre] = {
            "descripcion": p["descripcion"],
            "senales": sen,
            "propuesta": prop,
            "candidatos": {k: tabla(v) for k, v in candidatos.items() if k in buckets},
        }

    if guardar and not solo_perfil:
        guardar_salidas(resultado, paneles, macro)
    return resultado


def tabla(df: pd.DataFrame | None, n: int = 8) -> list[dict]:
    if df is None or df.empty:
        return []
    cols = [c for c in ("ticker", "tipo", "precio", "var_dia", "volumen", "vencimiento", "dias", "tir",
                        "ret_1m", "ret_3m", "ret_6m", "vol_anual", "rsi14", "sobre_sma200", "max_dd_6m",
                        "score", "apto", "motivo_descarte") if c in df.columns]
    out = df[cols].head(n).copy()
    if "vencimiento" in out:
        out["vencimiento"] = out["vencimiento"].astype(str)
    return json.loads(out.to_json(orient="records", force_ascii=False))


def guardar_salidas(res: dict, paneles: dict, macro: dict):
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "historial").mkdir(exist_ok=True)
    texto = json.dumps(res, ensure_ascii=False, indent=1, default=str)
    (SALIDA / "latest.json").write_text(texto, encoding="utf-8")
    (SALIDA / "historial" / f"{res['generado'][:10]}.json").write_text(texto, encoding="utf-8")

    precios = {}
    for df in paneles.values():
        if not df.empty:
            precios.update({t: float(p) for t, p in zip(df["ticker"], df["precio"]) if p and not math.isnan(p)})
    ruta_paper = SALIDA / "paper.json"
    estado = paper.cargar(ruta_paper)
    tasa_liq = (macro.get("tna_plazo_fijo") or 0) / 12
    propuestas = {n: v["propuesta"] for n, v in res["perfiles"].items()}
    estado = paper.actualizar(estado, propuestas, precios, macro.get("dolar_mep"), tasa_liq,
                              hoy=res["generado"][:10])
    ruta_paper.write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    (RAIZ / "reporte.md").write_text(reporte_md(res, estado), encoding="utf-8")


def fmt_ars(x):
    return "-" if x is None else f"$ {x:,.0f}".replace(",", ".")


def reporte_md(res: dict, estado: dict) -> str:
    m = res["macro"]
    L = [f"# Detector de oportunidades — {res['generado'][:10]}", "",
         "> Herramienta personal de análisis. No es asesoramiento financiero.", "",
         "## Contexto macro", ""]
    for k, etiqueta in (("inflacion_mensual", "Inflación último mes (%)"), ("tna_plazo_fijo", "TNA plazo fijo prom. (%)"),
                        ("dolar_oficial", "Dólar oficial"), ("dolar_mep", "Dólar MEP"), ("dolar_ccl", "Dólar CCL"),
                        ("riesgo_pais", "Riesgo país (pb)")):
        if k in m:
            L.append(f"- {etiqueta}: {m[k]}")
    for nombre, p in res["perfiles"].items():
        pr = p["propuesta"]
        L += ["", f"## Perfil {nombre}", "", p["descripcion"], ""]
        L += [f"- {n}" for n in p["senales"]["notas"]]
        L += ["", f"Propuesta para {fmt_ars(pr['monto'])}:", "", "| Bucket | Instrumento | Cantidad | Monto | Costo |",
              "|---|---|---|---|---|"]
        for pos in pr["posiciones"]:
            cant = "" if pos.get("cantidad") is None else f"{pos['cantidad']} {pos.get('unidad', '')}"
            L.append(f"| {pos['bucket']} | {pos['ticker']} | {cant} | {fmt_ars(pos.get('monto_bruto'))} | {fmt_ars(pos.get('costo'))} |")
        h = estado["perfiles"].get(nombre, {}).get("historial", [])
        if h:
            u = h[-1]
            L.append(f"\nPaper trading: valor {fmt_ars(u['valor'])} sobre {fmt_ars(u['aportado'])} aportados "
                     f"({u['rend']:+.2%}); mismos aportes en MEP: {fmt_ars(u['bench_mep'])}.")
    L += ["", "## Estado de fuentes", ""] + [f"- {k}: {v}" for k, v in res["fuentes"].items()]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--monto", type=float)
    ap.add_argument("--perfil", choices=["conservador", "moderado", "riesgoso"])
    ap.add_argument("--sin-historia", action="store_true")
    a = ap.parse_args()
    res = correr(a.monto, a.perfil, con_historia=not a.sin_historia, guardar=a.perfil is None and a.monto is None)
    if a.perfil or a.monto:
        print(json.dumps({n: p["propuesta"] for n, p in res["perfiles"].items()}, ensure_ascii=False, indent=1))
    else:
        print((RAIZ / "reporte.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

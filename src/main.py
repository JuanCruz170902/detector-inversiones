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

from . import backtest as BT
from . import balances as BAL
from . import curva as C
from . import empresas as EMP
from . import fuentes as F
from . import hard_dollar as HD
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
        "letras": reg.tomar("argdatos_letras", F.letras),
        "a3500_serie": reg.tomar("bcra_a3500_serie", F.bcra_serie, 5, 60),
        "bcra": reg.tomar("bcra", F.bcra_principales),
        "mep": reg.tomar("data912_mep", F.mep),
    }
    cal = reg.tomar("calendario_balances", BAL.proximos, perfiles.get("dias_sin_balance", 7))
    balances, fuente_bal = cal if cal else ({}, None)
    if fuente_bal:
        reg.estado["calendario_balances"] = f"ok ({fuente_bal}, {len(balances)} empresas)"
    paneles = {n: M.panel_a_df(reg.tomar(f"data912_{n}", F.panel, n) or []) for n in F.PANELES}
    macro = armar_macro(reg, raw)

    # ---- renta fija en pesos: curvas, breakevens, dollar linked ----
    hz = tuple(perfiles["horizonte_meses"])
    rf = M.renta_fija_pesos(paneles["bonos"], paneles["letras"], hz)
    fija = C.curva_tasa_fija(raw["letras"])
    cer = C.curva_cer(raw["bonos_cer"])
    a3500 = macro.get("bcra_a3500")
    dl = C.curva_dollar_linked(rf, a3500, fija)
    be = C.breakevens_inflacion(fija, cer)
    infl_esp = None
    if macro.get("bcra_rem_12m"):
        infl_esp = ((1 + macro["bcra_rem_12m"] / 100) ** (1 / 12) - 1) * 100
        macro["inflacion_esperada_fuente"] = "REM BCRA (mediana 12 meses)"
    elif macro.get("inflacion_3m_prom"):
        infl_esp = macro["inflacion_3m_prom"]
        macro["inflacion_esperada_fuente"] = "promedio últimos 3 meses"
    if infl_esp is not None:
        macro["inflacion_esperada_mensual"] = round(infl_esp, 2)
    curvas = {"breakeven": C.senal_breakeven(be, hz, infl_esp)}
    serie_a = raw.get("a3500_serie") or []
    if not dl.empty and len(serie_a) > 15:
        ult, ant = serie_a[-1], next((x for x in serie_a if x["fecha"] >= F.hace(31)), serie_a[0])
        dias = max((pd.Timestamp(ult["fecha"]) - pd.Timestamp(ant["fecha"])).days, 1)
        reciente = ((ult["valor"] / ant["valor"]) ** (30 / dias) - 1) * 100
        tramo = dl[dl["dias"].between(hz[0] * 30, hz[1] * 30)]
        implicita = float((tramo if not tramo.empty else dl)["devaluacion_be_mensual"].mean())
        estado = "barata" if implicita < reciente - 0.1 else ("cara" if implicita > reciente + 0.5 else "neutral")
        curvas["dl"] = {"implicita_mensual": round(implicita, 2), "reciente_mensual": round(reciente, 2), "estado": estado}
        macro["devaluacion_reciente_mensual"] = round(reciente, 2)
    if not dl.empty:
        dl["atractivo"] = -dl["devaluacion_be_mensual"]
    rank_rf = {"tasa_fija": C.ranking(fija, "tea", hz), "cer": C.ranking(cer, "tir", hz),
               "dollar_linked": C.ranking(dl, "atractivo", hz) if not dl.empty else dl}

    # ---- hard dollar: TIR en USD de los cortos ----
    bonos = paneles["bonos"]
    hd = pd.DataFrame()
    if not bonos.empty:
        px = dict(zip(bonos["ticker"], bonos["precio"]))
        vol = dict(zip(bonos["ticker"], bonos["volumen"]))
        filas = []
        for t in universo["hard_dollar"]:
            if not px.get(t):
                continue
            info = HD.tir(t, px.get(t + "D")) if px.get(t + "D") else None
            if info and not (-5 < info["tir"] < 40):
                info = None
            filas.append({"ticker": t, "precio": float(px[t]), "precio_usd": px.get(t + "D"),
                          "vol_ars": (vol.get(t) or 0) * px[t] / 100, **(info or {})})
        hd = pd.DataFrame(filas)
        if not hd.empty:
            if "tir" not in hd:
                hd["tir"] = float("nan")
            if "duration" not in hd:
                hd["duration"] = float("nan")
            dmax = perfiles.get("hard_dollar_duration_max", 3)
            liq = hd["vol_ars"] >= C.VOL_MIN_ARS
            corta = hd["duration"].fillna(99) <= dmax
            hd["apto"] = liq & corta
            hd["motivo_descarte"] = [", ".join(m for m, c in (("poca liquidez", not a), (f"duration > {dmax}", not b)) if c)
                                     for a, b in zip(liq, corta)]
            hd["_c"] = hd["tir"].notna()
            hd = hd.sort_values(["apto", "_c", "tir"], ascending=[False, False, False]).drop(columns="_c")

    # ---- renta variable: historia y métricas ----
    met = {"cedears_etf": {}, "cedears": {}, "acciones_arg": {}}
    series = {"cedears_etf": {}, "cedears": {}, "acciones_arg": {}}
    if con_historia:
        for grupo, tipo in (("cedears_etf", "cedears"), ("cedears", "cedears"), ("acciones_arg", "stocks")):
            for t in universo[grupo]:
                barras = reg.tomar(f"hist_{t}", F.historia, tipo, t)
                if not isinstance(barras, list) or not barras or not isinstance(barras[0], dict):
                    reg.estado[f"hist_{t}"] = "sin historia"  # ticker fuera de la lista de data912
                    barras = None
                met[grupo][t] = M.metricas_historia(barras) if barras else None
                if barras:
                    series[grupo][t] = M.serie(barras)
        # resumo el estado de las historias en una sola línea
        fallas = [k for k, v in reg.estado.items() if k.startswith("hist_") and v != "ok"]
        reg.estado = {k: v for k, v in reg.estado.items() if not k.startswith("hist_")}
        reg.estado["data912_historia"] = "ok" if not fallas else f"fallaron {len(fallas)}: {', '.join(f[5:] for f in fallas[:8])}"

    # ---- información por empresa: balances (SEC) y noticias ----
    emp = {}
    if con_historia:
        usa = reg.tomar("data912_usa", F.usa_precios) or {}
        tick = list(dict.fromkeys(universo["cedears"] + universo["acciones_arg"]))
        rel = reg.tomar("sec_y_noticias", EMP.relevar, tick, usa, tick)
        if rel:
            emp = rel["empresas"]
            con_bal = sum(1 for v in emp.values() if v.get("ultimo_balance"))
            con_not = sum(1 for v in emp.values() if v.get("noticias"))
            reg.estado["sec_y_noticias"] = f"ok ({con_bal} balances, {con_not} con noticias)" + (
                f"; {len(rel['errores'])} errores" if rel["errores"] else "")

    # ---- por perfil ----
    resultado = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "fuentes": reg.estado, "macro": macro, "perfiles": {}, "monto": monto,
                 "curvas": {"tasa_fija": tabla(fija, 40), "cer": tabla(cer, 40), "dollar_linked": tabla(dl, 20),
                            "hard_dollar": tabla(hd, 20), "breakevens": tabla(be, 20), "senales": curvas}}
    nombres = [solo_perfil] if solo_perfil else list(perfiles["perfiles"])
    for nombre in nombres:
        p = perfiles["perfiles"][nombre]
        sen = motor.senales_macro(macro, p, curvas)
        buckets = motor.ajustar_buckets(p, sen)
        filtros = p.get("filtros_renta_variable", {"solo_tendencia_alcista": True, "vol_max_anual": 0.35})
        cfg_s = perfiles["scoring_renta_variable"]
        rv = {
            "cedears_etf": motor.ranking_renta_variable(met["cedears_etf"], paneles["cedears"], cfg_s, filtros, M.score_renta_variable),
            "cedears": motor.ranking_renta_variable({**met["cedears_etf"], **met["cedears"]}, paneles["cedears"], cfg_s, filtros, M.score_renta_variable),
            "acciones_arg": motor.ranking_renta_variable(met["acciones_arg"], paneles["acciones"], cfg_s, filtros, M.score_renta_variable),
        }
        for k in rv:
            rv[k] = filtrar_balances(rv[k], balances)
            rv[k] = filtrar_calidad(rv[k], emp, perfiles.get("filtro_calidad", {}))
        if perfiles.get("modo_por_bucket", {}).get("acciones_arg") == "liquidez":
            rv["acciones_arg"] = filtrar_calidad(por_liquidez(rv["acciones_arg"], cfg_s), emp, perfiles.get("filtro_calidad", {}))
        candidatos = {**rank_rf, "hard_dollar": hd, **rv}
        prop = motor.proponer(nombre, p, buckets, candidatos, monto, perfiles["broker"])
        resultado["perfiles"][nombre] = {
            "descripcion": p["descripcion"],
            "senales": sen,
            "propuesta": prop,
            "candidatos": {k: tabla(v) for k, v in candidatos.items() if k in buckets},
        }

    resultado["empresas"] = emp
    if con_historia and not solo_perfil:
        badlar = reg.tomar("bcra_badlar_serie", F.bcra_serie, 7, 1600)
        tasa = pd.Series({pd.Timestamp(x["fecha"]): x["valor"] for x in badlar}).sort_index() if badlar else None
        resultado["backtest"] = correr_backtests(perfiles, series, tasa)
    if guardar and not solo_perfil:
        guardar_salidas(resultado, paneles, macro)
    return resultado


def filtrar_balances(df: pd.DataFrame, balances: dict[str, str]) -> pd.DataFrame:
    """Marca como no apto todo papel que presenta resultados en los próximos días."""
    if df is None or df.empty or not balances:
        return df
    d = df.copy()
    fechas = d["ticker"].map(lambda t: balances.get(BAL.a_eeuu(t) or "", None))
    d["balance"] = fechas
    hay = fechas.notna()
    d.loc[hay, "apto"] = False
    d.loc[hay, "motivo_descarte"] = [", ".join(x for x in (m, f"balance el {f}") if x)
                                     for m, f in zip(d.loc[hay, "motivo_descarte"], fechas[hay])]
    return d


def filtrar_calidad(df: pd.DataFrame, emp: dict, cfg: dict) -> pd.DataFrame:
    """Agrega las alertas de balance a cada papel y excluye según config (p. ej. pérdidas en 12 meses)."""
    if df is None or df.empty or not emp:
        return df
    d = df.copy()
    d["alertas"] = d["ticker"].map(lambda t: "; ".join(emp.get(t, {}).get("alertas", [])))
    if cfg.get("excluir_perdidas"):
        # solo con datos de menos de 15 meses: no se excluye por un balance viejo
        malo = d["ticker"].map(lambda t: (emp.get(t, {}).get("resultado_ttm") or 0) < 0 and EMP.reciente(emp.get(t, {})))
        d.loc[malo, "apto"] = False
        d.loc[malo, "motivo_descarte"] = [", ".join(x for x in (m, "pérdidas en 12 meses") if x)
                                          for m in d.loc[malo, "motivo_descarte"]]
    return d


def por_liquidez(df: pd.DataFrame, cfg_s: dict) -> pd.DataFrame:
    """Canasta diversificada: ordena por volumen operado, ignora el momentum."""
    if df is None or df.empty:
        return df
    d = df.copy()
    liq = d["volumen"].fillna(0) >= cfg_s["volumen_min_ars"]
    bal = d["balance"].notna() if "balance" in d else pd.Series(False, index=d.index)
    d["apto"] = liq & ~bal
    d["motivo_descarte"] = [", ".join(m for m, c in (("poca liquidez", not a), (f"balance el {f}", b)) if c)
                            for a, b, f in zip(liq, bal, d["balance"] if "balance" in d else [None] * len(d))]
    d["score"] = d["volumen"]
    return d.sort_values(["apto", "volumen"], ascending=[False, False])


def correr_backtests(perfiles: dict, series: dict, tasa_liquidez=None) -> dict:
    cfg_s = perfiles["scoring_renta_variable"]
    com = perfiles["broker"]["comision_acciones"] * (1 + perfiles["broker"]["iva_sobre_comision"]) + perfiles["broker"]["derechos_mercado"]
    filt_mod = perfiles["perfiles"]["moderado"]["filtros_renta_variable"]
    filt_rie = perfiles["perfiles"]["riesgoso"]["filtros_renta_variable"]
    casos = {
        "moderado_cedears_etf": (series["cedears_etf"], filt_mod, 2, "SPY"),
        "riesgoso_cedears": ({**series["cedears_etf"], **series["cedears"]}, filt_rie, 3, "SPY"),
        "riesgoso_acciones_arg": (series["acciones_arg"], filt_rie, 2, None),
    }
    out = {}
    # comparación de variantes de la regla (para decidir con datos qué parámetros usar)
    variantes = {
        "actual (12m)": (cfg_s, None, None),
        "v0.1 (3m+6m / vol, RSI)": ({"peso_ret_3m": 0.5, "peso_ret_6m": 0.5, "penalizar_rsi_mayor_a": 75, "penalizacion_rsi": 0.5}, None, None),
        "6m+12m / vol": ({"peso_ret_6m": 0.5, "peso_ret_12m": 0.5}, None, None),
        "actual, top 5": (cfg_s, 5, None),
        "actual, sin filtros": (cfg_s, None, {"vol_max_anual": 9}),
    }
    tabla_var = []
    for nombre, (ser, filt, n, bench) in casos.items():
        for vn, (cfg_v, n_v, filt_v) in variantes.items():
            try:
                r = BT.correr(ser, cfg_v, filt_v or filt, n_v or n, 2 * com, bench, tasa_liquidez=tasa_liquidez)
                if r:
                    e, b = r["estrategia"], r["bench"]
                    tabla_var.append({"caso": nombre, "variante": vn, "anual": e["anual"], "vol": e["vol_anual"],
                                      "max_dd": e["max_drawdown"], "bench_anual": b["anual"], "bench_dd": b["max_drawdown"],
                                      "ratio": round(e["anual"] / e["vol_anual"], 2) if e["vol_anual"] else None,
                                      "bench_ratio": round(b["anual"] / b["vol_anual"], 2) if b["vol_anual"] else None})
            except Exception:  # noqa: BLE001
                traceback.print_exc()
    out["_variantes"] = tabla_var
    for nombre, (ser, filt, n, bench) in casos.items():
        try:
            r = BT.correr(ser, cfg_s, filt, n, 2 * com, bench, tasa_liquidez=tasa_liquidez)  # compra + venta en cada rotación
            if r:
                out[nombre] = r
        except Exception:  # noqa: BLE001
            traceback.print_exc()
    return out


def tabla(df: pd.DataFrame | None, n: int = 8) -> list[dict]:
    if df is None or df.empty:
        return []
    cols = [c for c in ("ticker", "tipo", "precio", "var_dia", "volumen", "vol_ars", "vencimiento", "dias", "tir",
                        "tea", "tem", "ajuste", "residuo_pb", "liquido", "precio_usd", "duration", "proximo_pago",
                        "tea_fija_equiv", "a3500_breakeven", "devaluacion_be_mensual", "md", "residual", "paridad",
                        "monto_proximo_pago", "balance", "alertas",
                        "fija", "cer", "tea_fija", "tir_real_cer", "inflacion_be_anual", "inflacion_be_mensual",
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
    for k, etiqueta in (("inflacion_esperada_mensual", "Inflación esperada mensual (%)"),
                        ("devaluacion_reciente_mensual", "Devaluación A3500 último mes (%)")):
        if k in m:
            L.append(f"- {etiqueta}: {m[k]}")
    cv = res.get("curvas", {})
    if cv.get("breakevens"):
        L += ["", "## Curva en pesos: inflación implícita", "", "| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |", "|---|---|---|---|---|"]
        L += [f"| {b['fija']} | {b['tea_fija']}% | {b['cer']} | {b['tir_real_cer']}% | {b['inflacion_be_mensual']}% |" for b in cv["breakevens"]]
    if cv.get("hard_dollar"):
        L += ["", "## Soberanos en dólares", ""]
        L += [f"- {h['ticker']}: TIR {h.get('tir', '–')}% · duration {h.get('duration', '–')} · paridad {h.get('paridad', '–')}% · precio USD {h.get('precio_usd')}" for h in cv["hard_dollar"] if h.get("tir") is not None]
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
    E = res.get("empresas") or {}
    en_prop = {x["ticker"] for p in res["perfiles"].values() for x in p["propuesta"]["posiciones"] if x.get("ticker") in E}
    if en_prop:
        L += ["", "## Empresas en las propuestas", "", "| Empresa | Datos hasta | Margen neto | ROE | P/E | Alertas |", "|---|---|---|---|---|---|"]
        for t in sorted(en_prop):
            e = E[t]
            f = lambda k, d=0: "–" if e.get(k) is None else f"{e[k]:.{d}%}"  # noqa: E731
            L.append(f"| {t} ({e.get('empresa', '')}) | {e.get('periodo_hasta', '–')} {e.get('formulario', '')} | {f('margen_neto', 1)} | {f('roe')} | {e.get('pe', '–')} | {'; '.join(e.get('alertas', [])) or '–'} |")
        for t in sorted(en_prop):
            for n in (E[t].get("noticias") or [])[:3]:
                L.append(f"- {t}: {n['titulo']} ({n['fuente']}, {n.get('fecha')})")
    if res.get("backtest"):
        L += ["", "## Backtest de la regla de renta variable", "", "| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |", "|---|---|---|---|---|"]
        for k, b in res["backtest"].items():
            if k.startswith("_"):
                continue
            L.append(f"| {k} | {b['desde']} a {b['hasta']} | {b['estrategia']['anual']:+.1%} | {b['bench']['anual']:+.1%} ({b['benchmark']}) | {b['estrategia']['max_drawdown']:.1%} |")
    var = (res.get("backtest") or {}).get("_variantes")
    if var:
        L += ["", "### Variantes de la regla", "", "| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {v['caso']} | {v['variante']} | {v['anual']:+.1%} | {v['vol']:.1%} | {v['max_dd']:.1%} | {v['ratio']} | {v['bench_anual']:+.1%} | {v['bench_ratio']} |" for v in var]
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

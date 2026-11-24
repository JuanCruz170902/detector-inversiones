"""Motor de decisión: señales macro, ranking por bucket y propuesta de cartera por perfil."""
from __future__ import annotations

import math

import pandas as pd

# -------------------------- señales macro --------------------------

def senales_macro(macro: dict, cfg_perfil: dict) -> dict:
    """Devuelve señales legibles a partir de inflación, tasas y dólar."""
    s: dict = {"notas": []}
    infl = macro.get("inflacion_mensual")          # % último mes, ej 2.1
    tna_pf = macro.get("tna_plazo_fijo")           # % TNA promedio bancos, ej 32
    if infl is not None and tna_pf is not None:
        tem = tna_pf / 12
        s["tasa_real_mensual"] = round(tem - infl, 2)
        s["tasa_real_negativa"] = tem < infl
        s["notas"].append(
            f"Plazo fijo rinde {tem:.2f}% mensual vs inflación {infl:.2f}% → tasa real "
            f"{'NEGATIVA: conviene CER' if tem < infl else 'positiva: conviene tasa fija'}."
        )
    oficial, mep = macro.get("dolar_oficial"), macro.get("dolar_mep")
    if oficial and mep:
        brecha = mep / oficial - 1
        s["brecha"] = round(brecha, 4)
        umbral = cfg_perfil.get("ajustes", {}).get("brecha_alerta", 0.15)
        s["brecha_alta"] = brecha > umbral
        s["notas"].append(f"Brecha MEP/oficial {brecha:.1%}" + (" (alta: sumar cobertura)" if brecha > umbral else "."))
    if macro.get("riesgo_pais"):
        s["notas"].append(f"Riesgo país {macro['riesgo_pais']:.0f} pb.")
    return s


def ajustar_buckets(perfil: dict, senales: dict) -> dict:
    b = dict(perfil["buckets"])
    aj = perfil.get("ajustes", {})
    if "cer" in b and "tasa_fija" in b and "tasa_real_negativa" in senales:
        d = aj.get("rotacion_cer_tasa_fija", 0)
        if senales["tasa_real_negativa"]:
            d = min(d, b["tasa_fija"])
            b["cer"] += d
            b["tasa_fija"] -= d
        else:
            d = min(d, b["cer"])
            b["tasa_fija"] += d
            b["cer"] -= d
    if senales.get("brecha_alta") and "dollar_linked" in b and "liquidez" in b:
        d = min(aj.get("rotacion_dl", 0), b["liquidez"])
        b["dollar_linked"] += d
        b["liquidez"] -= d
    return {k: round(v, 4) for k, v in b.items() if v > 0}


# -------------------------- rankings --------------------------

def ranking_renta_fija(rf: pd.DataFrame, cer_tir: pd.DataFrame | None, horizonte=(1, 6)) -> dict[str, pd.DataFrame]:
    out = {}
    if rf is None or rf.empty:
        return out
    for tipo in ("tasa_fija", "dollar_linked", "tamar"):
        d = rf[rf["tipo"] == tipo].copy()
        # preferir lo que vence dentro del horizonte y es líquido
        d["orden"] = (~d["en_horizonte"]).astype(int)
        out[tipo] = d.sort_values(["orden", "volumen"], ascending=[True, False]).head(5)
    cer = rf[rf["tipo"] == "cer"].copy()
    if cer_tir is not None and not cer_tir.empty:
        cols = [c for c in ("ticker", "tir", "fechaVencimiento") if c in cer_tir.columns]
        cer = cer.merge(cer_tir[cols], on="ticker", how="left")
        if "fechaVencimiento" in cer:
            # los CER no traen el vencimiento en el ticker: lo tomo de ArgentinaDatos
            venc = pd.to_datetime(cer["fechaVencimiento"], errors="coerce")
            cer["vencimiento"] = venc.dt.date.where(venc.notna(), cer["vencimiento"])
            cer["dias"] = (venc - pd.Timestamp.today().normalize()).dt.days.where(venc.notna(), cer["dias"])
            lo, hi = horizonte
            cer["en_horizonte"] = cer["dias"].between(lo * 30, hi * 30)
            cer = cer[~(cer["dias"] < 15)]  # muy cerca del vencimiento: TIR poco confiable
        cer["orden"] = (~cer["en_horizonte"]).astype(int)
        # dentro del horizonte, mayor TIR real primero
        cer = cer.sort_values(["orden", "tir", "volumen"], ascending=[True, False, False])
    else:
        cer = cer.sort_values("volumen", ascending=False)
    out["cer"] = cer.head(5)
    return out


def ranking_renta_variable(metricas: dict[str, dict], panel: pd.DataFrame, cfg_score: dict,
                           filtros: dict, score_fn) -> pd.DataFrame:
    filas = []
    hay_panel = panel is not None and not panel.empty
    vol_por_ticker = dict(zip(panel["ticker"], panel["volumen"])) if hay_panel else {}
    px_por_ticker = dict(zip(panel["ticker"], panel["precio"])) if hay_panel else {}
    for t, m in metricas.items():
        if not m:
            continue
        fila = {"ticker": t, **m}
        if px_por_ticker.get(t):  # precio de pantalla de hoy si está, si no el último cierre histórico
            fila["precio"] = float(px_por_ticker[t])
        # data912 informa volumen en cantidad de papeles: lo paso a pesos
        fila["volumen"] = vol_por_ticker.get(t, math.nan) * fila["precio"]
        fila["score"] = score_fn(m, cfg_score)
        motivos = []
        if filtros.get("solo_tendencia_alcista") and m.get("sobre_sma200") is False:
            motivos.append("debajo de SMA200")
        if m["vol_anual"] > filtros.get("vol_max_anual", 9):
            motivos.append("volatilidad alta")
        if not math.isnan(fila["volumen"]) and fila["volumen"] < cfg_score["volumen_min_ars"]:
            motivos.append("poca liquidez")
        fila["apto"] = not motivos
        fila["motivo_descarte"] = ", ".join(motivos)
        filas.append(fila)
    df = pd.DataFrame(filas)
    if df.empty:
        return df
    return df.sort_values(["apto", "score"], ascending=[False, False])


# -------------------------- propuesta de cartera --------------------------

def costo_operacion(monto: float, es_bono: bool, broker: dict) -> float:
    com = broker["comision_bonos"] if es_bono else broker["comision_acciones"]
    return monto * (com * (1 + broker["iva_sobre_comision"]) + broker["derechos_mercado"])


def proponer(perfil_nombre: str, perfil: dict, buckets: dict, candidatos: dict[str, pd.DataFrame],
             monto: float, broker: dict) -> dict:
    """Reparte el monto entre buckets y elige instrumentos concretos respetando ticket mínimo
    y cantidad máxima de posiciones. Calcula cantidades enteras y costos."""
    ticket_min = broker["ticket_minimo"]
    max_pos = perfil["max_posiciones"]
    # cuántos instrumentos por bucket: 1 por defecto, 2-3 en renta variable si el monto lo permite
    asignaciones = []
    for bucket, peso in sorted(buckets.items(), key=lambda x: -x[1]):
        monto_b = monto * peso
        if bucket == "liquidez":
            asignaciones.append({"bucket": bucket, "ticker": "CAUCION/FCI MM", "monto": monto_b, "precio": None})
            continue
        cand = candidatos.get(bucket)
        if cand is None or cand.empty:
            asignaciones.append({"bucket": bucket, "ticker": None, "monto": monto_b, "precio": None,
                                 "nota": "sin datos: queda en liquidez"})
            continue
        if "apto" in cand:
            cand = cand[cand["apto"]]
            if cand.empty:
                asignaciones.append({"bucket": bucket, "ticker": None, "monto": monto_b, "precio": None,
                                     "nota": "ningún candidato pasó los filtros: queda en liquidez"})
                continue
        n = 1
        if bucket in ("cedears", "acciones_arg", "cedears_etf"):
            n = max(1, min(3, int(monto_b // ticket_min)))
        n = min(n, len(cand))
        for _, fila in cand.head(n).iterrows():
            asignaciones.append({"bucket": bucket, "ticker": fila["ticker"], "monto": monto_b / n,
                                 "precio": float(fila["precio"]), "score": _num(fila.get("score")),
                                 "tir": _num(fila.get("tir")), "vencimiento": _str(fila.get("vencimiento"))})

    # limitar posiciones: las más chicas se fusionan en liquidez
    asignaciones.sort(key=lambda a: -a["monto"])
    finales, a_liquidez = [], 0.0
    for a in asignaciones:
        reales = [x for x in finales if x["ticker"] and x["bucket"] != "liquidez"]
        if a["bucket"] == "liquidez" or a["ticker"] is None:
            a_liquidez += a["monto"]
        elif a["monto"] < ticket_min or len(reales) >= max_pos:
            a_liquidez += a["monto"]
        else:
            finales.append(a)

    # cantidades enteras: bonos/letras cotizan cada 100 VN
    total_costos, invertido = 0.0, 0.0
    for a in finales:
        es_bono = a["bucket"] in ("cer", "tasa_fija", "dollar_linked", "tamar", "hard_dollar")
        precio_unit = a["precio"] / 100 if es_bono else a["precio"]
        costo_pct = costo_operacion(1, es_bono, broker)
        cantidad = math.floor(a["monto"] / (precio_unit * (1 + costo_pct)))
        bruto = cantidad * precio_unit
        costo = costo_operacion(bruto, es_bono, broker)
        a.update({"cantidad": cantidad, "unidad": "VN" if es_bono else "acciones",
                  "monto_bruto": round(bruto, 2), "costo": round(costo, 2)})
        a_liquidez += a["monto"] - bruto - costo
        total_costos += costo
        invertido += bruto
    finales = [a for a in finales if a["cantidad"] > 0]  # no alcanzó para 1 unidad: quedó en liquidez
    finales.append({"bucket": "liquidez", "ticker": "CAUCION/FCI MM", "monto_bruto": round(a_liquidez, 2),
                    "cantidad": None, "costo": 0})
    return {
        "perfil": perfil_nombre,
        "monto": monto,
        "buckets": buckets,
        "posiciones": finales,
        "invertido": round(invertido, 2),
        "liquidez": round(a_liquidez, 2),
        "costos": round(total_costos, 2),
    }


def _num(x):
    try:
        return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 4)
    except (TypeError, ValueError):
        return None


def _str(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else str(x)

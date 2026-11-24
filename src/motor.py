"""Motor de decisión: señales macro, ranking por bucket y propuesta de cartera por perfil."""
from __future__ import annotations

import math

import pandas as pd

BUCKETS_BONO = ("cer", "tasa_fija", "dollar_linked", "tamar", "hard_dollar")

# -------------------------- señales macro --------------------------

def senales_macro(macro: dict, cfg_perfil: dict, curvas: dict | None = None) -> dict:
    """Señales legibles. `curvas` trae el breakeven de inflación y la señal de dollar linked."""
    curvas = curvas or {}
    s: dict = {"notas": []}
    be = curvas.get("breakeven") or {}
    if be:
        s["prefiere"] = be["prefiere"]
        texto = {"tasa_fija": "el mercado descuenta MÁS inflación de la esperada → conviene tasa fija",
                 "cer": "el mercado descuenta MENOS inflación de la esperada → conviene CER",
                 "neutral": "breakeven alineado con lo esperado → reparto neutral"}[be["prefiere"]]
        s["notas"].append(f"Inflación implícita {be['inflacion_implicita_mensual']:.2f}% mensual vs esperada "
                          f"{be['inflacion_esperada_mensual']:.2f}%: {texto}.")
    infl = macro.get("inflacion_mensual")
    tna_pf = macro.get("tna_plazo_fijo")
    if infl is not None and tna_pf is not None:
        tem = tna_pf / 12
        s["tasa_real_mensual"] = round(tem - infl, 2)
        s["tasa_real_negativa"] = tem < infl
        if not be:
            s["notas"].append(
                f"Plazo fijo rinde {tem:.2f}% mensual vs inflación {infl:.2f}% → tasa real "
                f"{'NEGATIVA: conviene CER' if tem < infl else 'positiva: conviene tasa fija'}.")
    dl = curvas.get("dl") or {}
    if dl:
        s["dl"] = dl["estado"]
        s["notas"].append(f"Dollar linked: devaluación implícita {dl['implicita_mensual']:.2f}% mensual vs "
                          f"{dl['reciente_mensual']:.2f}% del último mes → cobertura {dl['estado']}.")
    oficial, mep = macro.get("dolar_oficial"), macro.get("dolar_mep")
    if oficial and mep:
        brecha = mep / oficial - 1
        s["brecha"] = round(brecha, 4)
        umbral = cfg_perfil.get("ajustes", {}).get("brecha_alerta", 0.15)
        s["brecha_alta"] = brecha > umbral
        s["notas"].append(f"Brecha MEP/oficial {brecha:.1%}" + (" (alta: sumar cobertura)." if brecha > umbral else "."))
    if macro.get("riesgo_pais"):
        s["notas"].append(f"Riesgo país {macro['riesgo_pais']:.0f} pb.")
    return s


def _mover(b: dict, desde: str, hacia: str, d: float):
    if desde in b and hacia in b:
        d = min(d, b[desde])
        b[desde] -= d
        b[hacia] += d


def ajustar_buckets(perfil: dict, senales: dict) -> dict:
    b = dict(perfil["buckets"])
    aj = perfil.get("ajustes", {})
    rot = aj.get("rotacion_cer_tasa_fija", 0.10)
    pref = senales.get("prefiere")
    if pref == "tasa_fija":
        _mover(b, "cer", "tasa_fija", rot)
    elif pref == "cer":
        _mover(b, "tasa_fija", "cer", rot)
    elif pref is None and "tasa_real_negativa" in senales:  # respaldo si no hay curvas
        if senales["tasa_real_negativa"]:
            _mover(b, "tasa_fija", "cer", rot)
        else:
            _mover(b, "cer", "tasa_fija", rot)
    rot_dl = aj.get("rotacion_dl", 0.10)
    # si la cobertura ya está cara manda eso, aunque la brecha esté alta
    if senales.get("dl") == "cara":
        _mover(b, "dollar_linked", "tasa_fija", rot_dl)
    elif senales.get("dl") == "barata" or senales.get("brecha_alta"):
        _mover(b, "liquidez", "dollar_linked", rot_dl)
    return {k: round(v, 4) for k, v in b.items() if v > 1e-9}


# -------------------------- rankings --------------------------

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
        if fila["score"] <= 0:
            motivos.append("momentum negativo")
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
        es_bono = bucket in BUCKETS_BONO
        unit = cand["precio"] / (100 if es_bono else 1)
        n = max(1, min(3, int(monto_b // ticket_min))) if bucket in ("cedears", "acciones_arg", "cedears_etf") else 1
        elegidos = cand.iloc[0:0]
        while n >= 1:
            # sólo candidatos de los que se pueda comprar al menos una unidad con la parte que les toca
            elegidos = cand[unit <= (monto_b / n) * 0.99].head(n)
            if len(elegidos) == n:
                break
            n -= 1
        if elegidos.empty:
            asignaciones.append({"bucket": bucket, "ticker": None, "monto": monto_b, "precio": None,
                                 "nota": "el monto no alcanza para una unidad: queda en liquidez"})
            continue
        for _, fila in elegidos.iterrows():
            asignaciones.append({"bucket": bucket, "ticker": fila["ticker"], "monto": monto_b / n,
                                 "precio": float(fila["precio"]), "score": _num(fila.get("score")),
                                 "tir": _num(fila.get("tir", fila.get("tea"))), "vencimiento": _str(fila.get("vencimiento"))})

    # tope por posición: lo que exceda va a liquidez (evita concentrar el 40% en una sola acción)
    tope = monto * perfil.get("max_peso_posicion", 1.0)
    for a in list(asignaciones):
        if a["ticker"] and a["bucket"] != "liquidez" and a["monto"] > tope:
            asignaciones.append({"bucket": "liquidez", "ticker": "CAUCION/FCI MM", "monto": a["monto"] - tope, "precio": None})
            a["monto"] = tope

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
        es_bono = a["bucket"] in BUCKETS_BONO
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

"""Backtest mensual de la regla de renta variable (momentum ajustado por riesgo).

Cada fin de mes: se calculan las métricas con la historia disponible hasta ese día, se eligen los
N mejores que pasan los filtros del perfil y se mantienen con igual peso hasta el mes siguiente.
Se descuenta la comisión por rotación. Benchmark: comprar y mantener (SPY para CEDEARs; igual peso
del universo para acciones argentinas). Precios en pesos (los CEDEARs incluyen la variación del CCL)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .metricas import metricas_serie, score_renta_variable


def correr(series: dict[str, pd.Series], cfg_score: dict, filtros: dict, n: int, comision: float,
           benchmark: str | None = None, min_hist: int = 130) -> dict | None:
    series = {t: s for t, s in series.items() if s is not None and len(s) > min_hist}
    if len(series) < n + 1:
        return None
    precios = pd.DataFrame(series).sort_index().ffill()
    fines = precios.resample("ME").last().index
    fines = [f for f in fines if (precios.index <= f).sum() > min_hist]
    if len(fines) < 6:
        return None
    valor, bench, cartera = 1.0, 1.0, set()
    filas = []
    for f0, f1 in zip(fines[:-1], fines[1:]):
        hist = precios[precios.index <= f0]
        cand = []
        for t in precios.columns:
            s = hist[t].dropna()
            m = metricas_serie(s) if len(s) > min_hist else None
            if not m:
                continue
            sc = score_renta_variable(m, cfg_score)
            if sc <= 0:
                continue
            if filtros.get("solo_tendencia_alcista") and m.get("sobre_sma200") is False:
                continue
            if m["vol_anual"] > filtros.get("vol_max_anual", 9):
                continue
            cand.append((sc, t))
        elegidos = {t for _, t in sorted(cand, reverse=True)[:n]}
        p0 = precios[precios.index <= f0].iloc[-1]
        p1 = precios[precios.index <= f1].iloc[-1]
        if elegidos:
            rets = [(p1[t] / p0[t] - 1) for t in elegidos if p0[t] > 0 and not math.isnan(p1[t])]
            r = float(np.mean(rets)) if rets else 0.0
        else:
            r = 0.0  # sin candidatos: queda en liquidez (se asume 0 real, conservador)
        rotacion = len(elegidos ^ cartera) / max(len(elegidos | cartera), 1)
        valor *= (1 + r) * (1 - comision * rotacion)
        cartera = elegidos
        if benchmark and benchmark in precios:
            rb = p1[benchmark] / p0[benchmark] - 1
        else:
            rb = float(np.nanmean((p1 / p0 - 1).values))
        bench *= 1 + rb
        filas.append({"fecha": f1.date().isoformat(), "estrategia": round(valor, 4), "benchmark": round(bench, 4),
                      "ret_mes": round(r, 4), "ret_bench": round(float(rb), 4), "cartera": sorted(elegidos)})
    df = pd.DataFrame(filas)
    anios = len(df) / 12

    def stats(col, rcol):
        serie = df[col]
        dd = (serie / serie.cummax() - 1).min()
        return {"total": round(float(serie.iloc[-1] - 1), 4), "anual": round(float(serie.iloc[-1] ** (1 / anios) - 1), 4),
                "vol_anual": round(float(df[rcol].std() * math.sqrt(12)), 4), "max_drawdown": round(float(dd), 4)}

    return {"desde": df["fecha"].iloc[0], "hasta": df["fecha"].iloc[-1], "meses": len(df), "n": n,
            "benchmark": benchmark or "igual peso del universo",
            "estrategia": stats("estrategia", "ret_mes"), "bench": stats("benchmark", "ret_bench"),
            "meses_le_gana": int((df["ret_mes"] > df["ret_bench"]).sum()), "serie": filas}

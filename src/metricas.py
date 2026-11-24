"""Clasificación de instrumentos y métricas (renta variable y renta fija)."""
from __future__ import annotations

import re
from datetime import date

import numpy as np
import pandas as pd

MESES = {"E": 1, "F": 2, "M": 3, "A": 4, "Y": 5, "J": 6, "L": 7, "G": 8, "S": 9, "O": 10, "N": 11, "D": 12}
RE_LETRA = re.compile(r"^([STDM])(\d{2})([EFMAYJLGSOND])(\d)$")  # S31L6, T30J7, D30A6, M31G6


def vencimiento_desde_ticker(ticker: str) -> date | None:
    m = RE_LETRA.match(ticker)
    if not m:
        return None
    _, dia, mes, anio = m.groups()
    try:
        return date(2020 + int(anio), MESES[mes], int(dia))
    except ValueError:
        return None


def clasificar_renta_fija(ticker: str) -> str | None:
    """Clasifica por convención de tickers de BYMA. Devuelve None si no aplica."""
    t = ticker.upper()
    if t.startswith(("TZX", "TX", "DICP", "PARP", "CUAP", "TZXD")):
        return "cer"
    m = RE_LETRA.match(t)
    if m:
        return {"S": "tasa_fija", "T": "tasa_fija", "D": "dollar_linked", "M": "tamar"}[m.group(1)]
    if re.match(r"^T\d{2}[EFMAYJLGSOND]\d$", t):
        return "tasa_fija"
    return None


def panel_a_df(filas: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(filas)
    if df.empty:
        return df
    df = df.rename(columns={"symbol": "ticker", "c": "precio", "v": "volumen", "pct_change": "var_dia"})
    for col in ("precio", "volumen", "var_dia", "px_bid", "px_ask"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def renta_fija_pesos(df_bonos: pd.DataFrame, df_letras: pd.DataFrame, horizonte: tuple[int, int]) -> pd.DataFrame:
    """Une bonos y letras en pesos, clasifica, calcula días al vencimiento y TNA implícita cuando se puede."""
    df = pd.concat([df_bonos, df_letras], ignore_index=True)
    if df.empty:
        return df
    df = df[~df["ticker"].str.endswith(("D", "C"))]  # descarto especies en USD (MEP/CCL)
    df["tipo"] = df["ticker"].map(clasificar_renta_fija)
    df = df[df["tipo"].notna() & (df["precio"] > 0)].copy()
    df["vencimiento"] = df["ticker"].map(vencimiento_desde_ticker)
    hoy = date.today()
    df["dias"] = df["vencimiento"].map(lambda v: (v - hoy).days if v else np.nan)
    df = df[(df["dias"].isna()) | (df["dias"] > 5)]
    lo, hi = horizonte
    df["en_horizonte"] = df["dias"].between(lo * 30, hi * 30)
    return df.drop_duplicates("ticker")


def metricas_historia(barras: list[dict]) -> dict | None:
    if not barras or len(barras) < 60:
        return None
    s = pd.Series([b["c"] for b in barras], index=pd.to_datetime([b["date"] for b in barras])).sort_index()
    return metricas_serie(s[s > 0])


def serie(barras: list[dict]) -> pd.Series:
    s = pd.Series([b["c"] for b in barras], index=pd.to_datetime([b["date"] for b in barras])).sort_index()
    s = s[s > 0]
    return s[~s.index.duplicated(keep="last")]


def metricas_serie(s: pd.Series) -> dict | None:
    if len(s) < 60:
        return None
    ret = s.pct_change().dropna()

    def r(n):
        return float(s.iloc[-1] / s.iloc[-n - 1] - 1) if len(s) > n else np.nan

    delta = s.diff()
    sube = delta.clip(lower=0).rolling(14).mean()
    baja = (-delta.clip(upper=0)).rolling(14).mean()
    rsi = 100 - 100 / (1 + sube / baja.replace(0, np.nan))
    sma200 = s.rolling(200).mean().iloc[-1] if len(s) >= 200 else np.nan
    pico = s.iloc[-126:].cummax()
    return {
        "precio": float(s.iloc[-1]),
        "fecha": s.index[-1].date().isoformat(),
        "ret_1m": r(21),
        "ret_3m": r(63),
        "ret_6m": r(126),
        "vol_anual": float(ret.iloc[-63:].std() * np.sqrt(252)),
        "rsi14": float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else np.nan,
        "sobre_sma200": bool(s.iloc[-1] > sma200) if not np.isnan(sma200) else None,
        "max_dd_6m": float((s.iloc[-126:] / pico - 1).min()),
    }


def score_renta_variable(m: dict, cfg: dict) -> float:
    mom = cfg["peso_ret_3m"] * np.nan_to_num(m["ret_3m"]) + cfg["peso_ret_6m"] * np.nan_to_num(m["ret_6m"])
    vol = max(m["vol_anual"], 0.10)
    score = mom / vol
    if m.get("rsi14") and m["rsi14"] > cfg["penalizar_rsi_mayor_a"] and score > 0:
        score *= cfg["penalizacion_rsi"]
    return float(score)

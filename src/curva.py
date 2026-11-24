"""Curvas de renta fija en pesos y breakevens.

- Tasa fija (LECAP/BONCAP): TEA/TEM de ArgentinaDatos (/finanzas/letras).
- CER: TIR real de ArgentinaDatos (/finanzas/bonos-cer).
- Dollar linked: devaluación implícita a partir del precio y el A3500.
- Valor relativo: residuo de cada instrumento contra una curva ajustada (TEA ~ a + b·ln(días)).
- Breakeven de inflación: (1+TEA fija)/(1+TIR real CER) − 1 para vencimientos parecidos.
"""
from __future__ import annotations

import math
from datetime import date

import numpy as np
import pandas as pd

DIAS_MIN = 30          # por debajo, la TIR es poco confiable (lag del CER, liquidación)
VOL_MIN_ARS = 20e6     # volumen operado mínimo para considerar comprable un bono


def _dias(venc) -> float:
    try:
        return (pd.Timestamp(venc).date() - date.today()).days
    except Exception:  # noqa: BLE001
        return math.nan


def curva_tasa_fija(letras: dict | None) -> pd.DataFrame:
    if not letras:
        return pd.DataFrame()
    df = pd.DataFrame(letras.get("letras", []))
    if df.empty:
        return df
    df = df.rename(columns={"precioArs": "precio", "teaPorcentaje": "tea", "temPorcentaje": "tem",
                            "tnaPorcentaje": "tna", "fechaVencimiento": "vencimiento"})
    df["dias"] = df["vencimiento"].map(_dias)
    df["vol_ars"] = pd.to_numeric(df.get("volumenEfectivoArs"), errors="coerce")
    df = df[(df["dias"] >= DIAS_MIN) & df["tea"].notna()].copy()
    df["tipo"] = "tasa_fija"
    return _valor_relativo(df, "tea")


def curva_cer(bonos_cer: dict | None) -> pd.DataFrame:
    if not bonos_cer:
        return pd.DataFrame()
    df = pd.DataFrame(bonos_cer.get("bonos", []))
    if df.empty:
        return df
    df = df.rename(columns={"precioArs": "precio", "tirPorcentaje": "tir", "fechaVencimiento": "vencimiento"})
    df["dias"] = df["vencimiento"].map(_dias)
    # los bonos CER cotizan cada 100 VN: volumen nominal × precio / 100
    df["vol_ars"] = pd.to_numeric(df["volumen"], errors="coerce") * df["precio"] / 100
    df = df[(df["dias"] >= DIAS_MIN) & df["tir"].notna()].copy()
    df["tipo"] = "cer"
    return _valor_relativo(df, "tir")


def _valor_relativo(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Ajusta col ~ a + b·ln(días) con los papeles líquidos y guarda el residuo en puntos básicos.
    Residuo positivo = paga más que la curva (barato)."""
    df = df.sort_values("dias").reset_index(drop=True)
    liq = df[df["vol_ars"] >= VOL_MIN_ARS]
    base = liq if len(liq) >= 3 else df
    if len(base) >= 3:
        x, y = np.log(base["dias"].astype(float)), base[col].astype(float)
        b, a = np.polyfit(x, y, 1)
        df["ajuste"] = a + b * np.log(df["dias"].astype(float))
        df["residuo_pb"] = ((df[col] - df["ajuste"]) * 100).round(0)
    else:
        df["ajuste"], df["residuo_pb"] = np.nan, np.nan
    df["liquido"] = df["vol_ars"] >= VOL_MIN_ARS
    return df


def curva_dollar_linked(rf: pd.DataFrame, a3500: float | None, fija: pd.DataFrame) -> pd.DataFrame:
    """Para cada letra DL: devaluación breakeven contra la tasa fija del mismo plazo.
    Si el A3500 al vencimiento supera ese valor, el DL rinde más que la tasa fija."""
    if rf is None or rf.empty or not a3500 or fija.empty:
        return pd.DataFrame()
    dl = rf[rf["tipo"] == "dollar_linked"].copy()
    if dl.empty:
        return dl
    dl = dl[dl["dias"] >= DIAS_MIN]
    filas = []
    for _, r in dl.iterrows():
        tea = float(np.interp(np.log(r["dias"]), np.log(fija["dias"].astype(float)), fija["tea"].astype(float)))
        ret_fija = (1 + tea / 100) ** (r["dias"] / 365) - 1
        # el DL paga VN × A3500 final: precio por 100 VN en pesos
        a3500_be = r["precio"] / 100 * (1 + ret_fija)
        dev_total = a3500_be / a3500 - 1
        filas.append({**r.to_dict(), "tea_fija_equiv": round(tea, 2),
                      "a3500_breakeven": round(a3500_be, 2),
                      "devaluacion_be_mensual": round(((1 + dev_total) ** (30 / r["dias"]) - 1) * 100, 2),
                      "vol_ars": r.get("volumen", 0) * r["precio"] / 100})
    out = pd.DataFrame(filas)
    out["liquido"] = out["vol_ars"] >= VOL_MIN_ARS
    return out.sort_values("dias")


def breakevens_inflacion(fija: pd.DataFrame, cer: pd.DataFrame, max_gap_dias: int = 45) -> pd.DataFrame:
    """Empareja cada letra de tasa fija con el CER de vencimiento más cercano."""
    if fija.empty or cer.empty:
        return pd.DataFrame()
    filas = []
    cer_ok = cer[cer["liquido"]] if cer["liquido"].sum() >= 2 else cer
    for _, f in fija.iterrows():
        gap = (cer_ok["dias"] - f["dias"]).abs()
        if gap.empty or gap.min() > max_gap_dias:
            continue
        c = cer_ok.loc[gap.idxmin()]
        infl_anual = (1 + f["tea"] / 100) / (1 + c["tir"] / 100) - 1
        filas.append({"fija": f["ticker"], "cer": c["ticker"], "dias": int(f["dias"]),
                      "tea_fija": f["tea"], "tir_real_cer": c["tir"],
                      "inflacion_be_anual": round(infl_anual * 100, 2),
                      "inflacion_be_mensual": round(((1 + infl_anual) ** (1 / 12) - 1) * 100, 2)})
    return pd.DataFrame(filas)


def senal_breakeven(be: pd.DataFrame, horizonte: tuple[int, int], infl_esperada_mensual: float | None,
                    margen_pp: float = 0.15) -> dict:
    """Compara la inflación que descuenta el mercado (en el horizonte) contra la esperada.
    Si el mercado descuenta MÁS inflación de la esperada → conviene tasa fija; si descuenta MENOS → CER."""
    if be.empty or infl_esperada_mensual is None:
        return {}
    lo, hi = horizonte
    tramo = be[be["dias"].between(lo * 30, hi * 30 + 60)]
    if tramo.empty:
        tramo = be
    implicita = float(tramo["inflacion_be_mensual"].mean())
    dif = implicita - infl_esperada_mensual
    if dif > margen_pp:
        prefer = "tasa_fija"
    elif dif < -margen_pp:
        prefer = "cer"
    else:
        prefer = "neutral"
    return {"inflacion_implicita_mensual": round(implicita, 2), "inflacion_esperada_mensual": round(infl_esperada_mensual, 2),
            "diferencia_pp": round(dif, 2), "prefiere": prefer}


def ranking(df: pd.DataFrame, col_rend: str, horizonte: tuple[int, int]) -> pd.DataFrame:
    """Orden: comprables y dentro del horizonte primero; luego más baratos contra la curva; luego mayor rendimiento."""
    if df.empty:
        return df
    lo, hi = horizonte
    d = df.copy()
    d["en_horizonte"] = d["dias"].between(lo * 30, hi * 30)
    d["apto"] = d["liquido"]
    d["motivo_descarte"] = np.where(d["liquido"], "", "poca liquidez")
    d["_rv"] = d["residuo_pb"].fillna(0) if "residuo_pb" in d else 0
    return d.sort_values(["apto", "en_horizonte", "_rv", col_rend], ascending=[False, False, False, False]).drop(columns="_rv")

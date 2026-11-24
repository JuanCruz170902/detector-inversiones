"""Calendario de presentación de resultados (balances) para excluir papeles con balance inminente.

Fuentes, en orden:
1. Nasdaq (api.nasdaq.com/api/calendar/earnings), público y sin clave: un request por día hábil.
2. Alpha Vantage EARNINGS_CALENDAR, solo si existe la variable de entorno ALPHAVANTAGE_API_KEY
   (en GitHub: Settings → Secrets → Actions).
Si ninguna responde, el filtro queda inactivo y el informe lo avisa (no se inventan fechas).
"""
from __future__ import annotations

import csv
import io
import os
import time
from datetime import date, timedelta

import requests

# ticker local (BYMA) → ticker en EE.UU. cuando difiere
MAPA_EEUU = {"BRKB": "BRK.B", "YPFD": "YPF", "PAMP": "PAM", "TGSU2": "TGS", "CRES": "CRESY", "TXAR": None,
             "ALUA": None, "TGNO4": None, "COME": None, "TRAN": None, "VALO": None, "MIRG": None, "BYMA": None}
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
     "Accept": "application/json, text/plain, */*", "Origin": "https://www.nasdaq.com", "Referer": "https://www.nasdaq.com/"}


def a_eeuu(ticker: str) -> str | None:
    return MAPA_EEUU.get(ticker, ticker)


def _dias_habiles(desde: date, n: int):
    d = desde
    while n > 0:
        if d.weekday() < 5:
            yield d
            n -= 1
        d += timedelta(days=1)


def nasdaq(dias: int = 7) -> dict[str, str]:
    out, ok = {}, 0
    for d in _dias_habiles(date.today(), dias):
        try:
            r = requests.get("https://api.nasdaq.com/api/calendar/earnings", params={"date": d.isoformat()},
                             headers=H, timeout=(5, 15))
            r.raise_for_status()
            filas = ((r.json() or {}).get("data") or {}).get("rows") or []
            ok += 1
            for f in filas:
                s = str(f.get("symbol", "")).upper()
                if s and s not in out:
                    out[s] = d.isoformat()
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.4)
    if ok == 0:
        raise RuntimeError("Nasdaq no respondió")
    return out


def alpha_vantage(dias: int = 7) -> dict[str, str]:
    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not key:
        raise RuntimeError("sin ALPHAVANTAGE_API_KEY")
    r = requests.get("https://www.alphavantage.co/query", params={"function": "EARNINGS_CALENDAR", "horizon": "3month",
                                                                  "apikey": key}, timeout=30)
    r.raise_for_status()
    limite = (date.today() + timedelta(days=dias + 2)).isoformat()
    out = {}
    for f in csv.DictReader(io.StringIO(r.text)):
        fecha = f.get("reportDate", "")
        if fecha and fecha <= limite:
            out[f["symbol"].upper()] = fecha
    if not out and "symbol" not in r.text[:200]:
        raise RuntimeError("Alpha Vantage sin datos: " + r.text[:120])
    return out


def proximos(dias: int = 7) -> tuple[dict[str, str], str]:
    """Devuelve ({ticker EE.UU.: fecha}, fuente)."""
    errores = []
    for nombre, fn in (("nasdaq", nasdaq), ("alpha_vantage", alpha_vantage)):
        try:
            return fn(dias), nombre
        except Exception as e:  # noqa: BLE001
            errores.append(f"{nombre}: {e}"[:120])
    raise RuntimeError("; ".join(errores))

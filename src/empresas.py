"""Información por empresa: balances (SEC EDGAR) y titulares de noticias (Yahoo Finance / Google News).

Balances: API pública de la SEC (data.sec.gov/api/xbrl/companyfacts). Cubre a las empresas de EE.UU.
(10-K/10-Q, US-GAAP, en USD) y a las argentinas con ADR (20-F/6-K, IFRS, en pesos ajustados por inflación).
Métricas de los últimos 12 meses (TTM): ventas, resultado neto, margen, ROE, deuda/patrimonio, flujo de caja
libre, crecimiento interanual de ventas (solo USD) y P/E con el precio en dólares de data912.

La SEC pide un User-Agent con contacto: se usa la variable de entorno SEC_USER_AGENT si existe.
"""
from __future__ import annotations

import os
import re
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime

import requests

from .balances import a_eeuu

UA_SEC = {"User-Agent": os.environ.get("SEC_USER_AGENT", "detector-inversiones research-bot"),
          "Accept-Encoding": "gzip, deflate"}
NAV = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

CONCEPTOS = {
    "ventas": [("us-gaap", "Revenues"), ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
               ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax"),
               ("us-gaap", "SalesRevenueNet"), ("us-gaap", "RevenuesNetOfInterestExpense"), ("ifrs-full", "Revenue"),
               ("ifrs-full", "RevenueFromContractsWithCustomers"), ("ifrs-full", "InterestRevenueCalculatedUsingEffectiveInterestMethod")],
    "resultado": [("us-gaap", "NetIncomeLoss"), ("us-gaap", "ProfitLoss"), ("ifrs-full", "ProfitLossAttributableToOwnersOfParent"),
                  ("ifrs-full", "ProfitLoss")],
    "patrimonio": [("us-gaap", "StockholdersEquity"), ("us-gaap", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
                   ("ifrs-full", "EquityAttributableToOwnersOfParent"), ("ifrs-full", "Equity")],
    "pasivo": [("us-gaap", "Liabilities"), ("ifrs-full", "Liabilities")],
    "flujo_operativo": [("us-gaap", "NetCashProvidedByUsedInOperatingActivities"), ("ifrs-full", "CashFlowsFromUsedInOperatingActivities")],
    "capex": [("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment"), ("ifrs-full", "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities")],
    "bpa": [("us-gaap", "EarningsPerShareDiluted"), ("us-gaap", "EarningsPerShareBasic")],
}
STOCK = {"patrimonio", "pasivo"}
FORMULARIOS = ("10-K", "10-Q", "20-F", "6-K", "40-F")            # saldos (a una fecha), no flujos
# entidades que cambiaron de registrante en la SEC: se suma la historia de la anterior
CIK_ANTERIOR = {"XOM": 34088}      # Exxon Mobil Corp → Exxonmobil Holdings Corp (2026)
FINANCIERAS = {"GGAL", "BMA", "BBAR", "SUPV", "JPM", "V", "BRK.B", "BYMA"}   # deuda/patrimonio no aplica igual
NOMBRES_AR = {"GGAL": "Grupo Financiero Galicia", "YPF": "YPF", "PAM": "Pampa Energía", "BMA": "Banco Macro",
              "BBAR": "BBVA Argentina", "CEPU": "Central Puerto", "TGS": "Transportadora de Gas del Sur",
              "LOMA": "Loma Negra", "CRESY": "Cresud", "EDN": "Edenor", "SUPV": "Grupo Supervielle"}


# ------------------------------- SEC -------------------------------

_CIKS: dict | None = None


def ciks() -> dict[str, tuple[int, str]]:
    global _CIKS
    if _CIKS is None:
        r = requests.get("https://www.sec.gov/files/company_tickers.json", headers=UA_SEC, timeout=30)
        r.raise_for_status()
        _CIKS = {v["ticker"].upper().replace("-", "."): (int(v["cik_str"]), v["title"]) for v in r.json().values()}
    return _CIKS


def _unir(viejo: dict, nuevo: dict) -> dict:
    """Une dos companyfacts concepto por concepto (el nuevo pisa en fechas repetidas)."""
    out = {tax: {c: {"units": {u: list(v) for u, v in d["units"].items()}} for c, d in cs.items()} for tax, cs in viejo.items()}
    for tax, cs in nuevo.items():
        for c, d in cs.items():
            dst = out.setdefault(tax, {}).setdefault(c, {"units": {}})["units"]
            for u, v in d["units"].items():
                dst.setdefault(u, []).extend(v)
    return out


def _dur(e) -> int | None:
    if "start" not in e:
        return None
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days


def _serie(facts: dict, clave: str):
    """Devuelve (entradas, unidad, taxonomía) del primer concepto con datos recientes."""
    mejor = None
    for tax, c in CONCEPTOS[clave]:
        x = facts.get(tax, {}).get(c)
        if not x:
            continue
        for unidad, entradas in x["units"].items():
            if not entradas:
                continue
            ultimo = max(e["end"] for e in entradas)
            if mejor is None or ultimo > mejor[3]:
                mejor = (entradas, unidad, tax, ultimo)
    return mejor


def _ttm(entradas: list[dict]) -> tuple[float, str] | None:
    """Últimos 12 meses: anual más reciente, o anual + acumulado del año actual − acumulado del año anterior."""
    dedup = {}
    for e in entradas:
        d = _dur(e)
        if d is None:
            continue
        dedup[(e["start"], e["end"])] = e        # la última presentación pisa a las anteriores
    anuales = sorted([e for e in dedup.values() if 350 <= _dur(e) <= 380], key=lambda e: e["end"])
    if not anuales:
        return None
    fy = anuales[-1]
    parciales = sorted([e for e in dedup.values() if 80 <= _dur(e) < 350 and e["end"] > fy["end"]], key=lambda e: (e["end"], _dur(e)))
    if not parciales:
        return float(fy["val"]), fy["end"]
    ytd = max((e for e in parciales if e["end"] == parciales[-1]["end"]), key=_dur)
    fin_prev = (date.fromisoformat(ytd["end"]) - timedelta(days=365))
    previo = [e for e in dedup.values() if abs(_dur(e) - _dur(ytd)) <= 10 and
              abs((date.fromisoformat(e["end"]) - fin_prev).days) <= 10]
    if not previo:
        return float(fy["val"]), fy["end"]
    return float(fy["val"]) + float(ytd["val"]) - float(previo[0]["val"]), ytd["end"]


def _ttm_hace_un_anio(entradas: list[dict], fin: str) -> float | None:
    objetivo = date.fromisoformat(fin) - timedelta(days=365)
    viejas = [e for e in entradas if date.fromisoformat(e["end"]) <= objetivo + timedelta(days=10)]
    r = _ttm(viejas)
    return r[0] if r and abs((date.fromisoformat(r[1]) - objetivo).days) <= 15 else None


def _saldo(entradas: list[dict]) -> tuple[float, str] | None:
    s = [e for e in entradas if "start" not in e]
    if not s:
        return None
    e = max(s, key=lambda e: (e["end"], e.get("filed", "")))
    return float(e["val"]), e["end"]


def fundamentals(ticker_local: str, precios_usd: dict[str, float] | None = None) -> dict | None:
    t_us = a_eeuu(ticker_local)
    if not t_us:
        return None
    info = ciks().get(t_us.upper())
    if not info:
        return None
    cik, nombre = info
    r = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json", headers=UA_SEC, timeout=30)
    r.raise_for_status()
    facts = r.json().get("facts", {})
    if t_us in CIK_ANTERIOR:
        try:
            r2 = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK_ANTERIOR[t_us]:010d}.json", headers=UA_SEC, timeout=30)
            r2.raise_for_status()
            facts = _unir(r2.json().get("facts", {}), facts)
        except Exception:  # noqa: BLE001
            pass
    out = {"ticker": ticker_local, "ticker_eeuu": t_us, "empresa": nombre.title(), "cik": cik}
    ultimo_filed, ultimo_form = "", ""
    for clave in CONCEPTOS:
        candidatos = []
        for tax, c in CONCEPTOS[clave]:
            x = facts.get(tax, {}).get(c)
            if not x:
                continue
            for unidad, entradas in x["units"].items():
                if not entradas:
                    continue
                v = _saldo(entradas) if clave in STOCK else _ttm(entradas)
                if v:
                    candidatos.append((v[1], v[0], entradas, unidad, tax))
        if not candidatos:
            continue
        fin, valor, entradas, unidad, tax = max(candidatos, key=lambda c: c[0])   # el dato más reciente
        out.setdefault("moneda", unidad.split("/")[0])
        out.setdefault("norma", "US-GAAP" if tax == "us-gaap" else "IFRS")
        for e in entradas:
            if e.get("form", "").startswith(FORMULARIOS) and e.get("filed", "") > ultimo_filed and e["end"] == fin:
                ultimo_filed, ultimo_form = e["filed"], e["form"]
        if clave in STOCK:
            out[clave] = valor
        else:
            out[clave + "_ttm"] = valor
            out["periodo_hasta"] = max(out.get("periodo_hasta", ""), fin)
            if clave == "ventas":
                prev = _ttm_hace_un_anio(entradas, fin)
                if prev:
                    out["ventas_crec_interanual"] = round(valor / prev - 1, 4)
    if out.get("pasivo") is None:
        # algunas empresas no informan el pasivo total: pasivo = activo (= pasivo + PN) − PN
        x = facts.get("us-gaap", {}).get("LiabilitiesAndStockholdersEquity")
        if x and out.get("patrimonio") is not None:
            v = _saldo(list(x["units"].values())[0])
            if v:
                out["pasivo"] = v[0] - out["patrimonio"]
    out["ultimo_balance"] = ultimo_filed
    out["formulario"] = ultimo_form
    # ratios
    res, ven, pat = out.get("resultado_ttm"), out.get("ventas_ttm"), out.get("patrimonio")
    if res is not None and ven:
        out["margen_neto"] = round(res / ven, 4)
    if res is not None and pat and pat > 0:
        out["roe"] = round(res / pat, 4)
    if out.get("pasivo") and pat and pat > 0 and t_us not in FINANCIERAS:
        out["deuda_patrimonio"] = round(out["pasivo"] / pat, 2)
    if out.get("flujo_operativo_ttm") is not None:
        out["fcf_ttm"] = out["flujo_operativo_ttm"] - (out.get("capex_ttm") or 0)
    if out.get("moneda") == "USD" and out.get("bpa_ttm") and precios_usd:
        px = precios_usd.get(t_us) or precios_usd.get(t_us.replace(".", ""))
        if px and out["bpa_ttm"] > 0:
            out["precio_usd"] = px
            out["pe"] = round(px / out["bpa_ttm"], 1)
    if out.get("moneda") != "USD":
        out.pop("ventas_crec_interanual", None)     # en pesos el crecimiento nominal no es comparable
    out["alertas"] = alertas(out)
    return out


def reciente(f: dict, meses: int = 15) -> bool:
    """El último período informado tiene menos de `meses` (los 20-F de ADRs argentinos son anuales)."""
    return bool(f.get("periodo_hasta")) and f["periodo_hasta"] >= (date.today() - timedelta(days=30 * meses)).isoformat()


def alertas(f: dict) -> list[str]:
    a = []
    if f.get("resultado_ttm") is not None and f["resultado_ttm"] < 0:
        a.append("pérdidas en los últimos 12 meses" if reciente(f) else "pérdidas en el último ejercicio informado")
    if f.get("ventas_crec_interanual") is not None and f["ventas_crec_interanual"] < -0.10:
        a.append(f"ventas {f['ventas_crec_interanual']:.0%} interanual")
    if f.get("deuda_patrimonio") and f["deuda_patrimonio"] > 4:
        a.append(f"endeudamiento alto (pasivo/patrimonio {f['deuda_patrimonio']})")
    if f.get("patrimonio") is not None and f["patrimonio"] <= 0:
        a.append("patrimonio negativo")
    if f.get("periodo_hasta") and not reciente(f):
        a.append(f"último dato en la SEC: {f['periodo_hasta']}")
    return a


# ------------------------------- Noticias -------------------------------

def _rss(url: str, n: int, dias: int) -> list[dict]:
    r = requests.get(url, headers=NAV, timeout=(5, 15))
    r.raise_for_status()
    raiz = ET.fromstring(r.content)
    limite = datetime.now().astimezone() - timedelta(days=dias)
    out = []
    for it in raiz.iter("item"):
        titulo = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        fuente = (it.findtext("source") or "").strip()
        try:
            fecha = parsedate_to_datetime(it.findtext("pubDate") or "")
        except Exception:  # noqa: BLE001
            fecha = None
        if fecha and fecha < limite:
            continue
        if not fuente and " - " in titulo:           # Google News: "Título - Medio"
            titulo, fuente = titulo.rsplit(" - ", 1)
        out.append({"titulo": re.sub(r"\s+", " ", titulo), "fuente": fuente or "Yahoo Finance", "link": link,
                    "fecha": fecha.date().isoformat() if fecha else None})
        if len(out) >= n:
            break
    return out


def noticias(ticker_local: str, n: int = 4, dias: int = 4) -> list[dict]:
    t_us = a_eeuu(ticker_local)
    if t_us in NOMBRES_AR or (t_us is None):
        nombre = NOMBRES_AR.get(t_us or "", ticker_local)
        q = requests.utils.quote(f'"{nombre}" acciones OR balance OR resultados')
        return _rss(f"https://news.google.com/rss/search?q={q}&hl=es-419&gl=AR&ceid=AR:es-419", n, dias)
    return _rss(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={t_us}&region=US&lang=en-US", n, dias)


# ------------------------------- Todo junto -------------------------------

def relevar(tickers: list[str], precios_usd: dict[str, float] | None = None, con_noticias: list[str] | None = None) -> dict:
    out, errores = {}, []
    for t in tickers:
        try:
            f = fundamentals(t, precios_usd)
            if f:
                out[t] = f
        except Exception as e:  # noqa: BLE001
            errores.append(f"{t}: {e}"[:80])
        time.sleep(0.15)                              # la SEC permite hasta 10 req/s
    for t in con_noticias or []:
        try:
            out.setdefault(t, {"ticker": t})["noticias"] = noticias(t)
        except Exception as e:  # noqa: BLE001
            errores.append(f"noticias {t}: {e}"[:80])
        time.sleep(0.3)
    return {"empresas": out, "errores": errores}

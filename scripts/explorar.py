"""Relevamiento de fuentes de información por empresa (corre en GitHub Actions).
La SEC pide un User-Agent con un contacto: se toma de la variable SEC_USER_AGENT (secreto del repo) si existe."""
import json
import os
from pathlib import Path

import requests

OUT = Path("docs/data/explorar")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": os.environ.get("SEC_USER_AGENT", "detector-inversiones research-bot"),
      "Accept-Encoding": "gzip, deflate"}
BROWSER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
res = {}


def probar(nombre, url, headers, recorte=1500, fn=None):
    try:
        r = requests.get(url, headers=headers, timeout=(5, 20))
        cuerpo = fn(r) if fn and r.ok else r.text[:recorte]
        res[nombre] = {"status": r.status_code, "bytes": len(r.content), "muestra": cuerpo}
    except Exception as e:  # noqa: BLE001
        res[nombre] = {"error": str(e)}


def resumen_facts(r):
    j = r.json()
    g = j.get("facts", {})
    out = {"entidad": j.get("entityName"), "taxonomias": list(g)}
    for tax, conceptos in g.items():
        out[tax] = sorted(conceptos)[:400]
    for tax in ("us-gaap", "ifrs-full"):
        for c in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "Revenue", "ProfitLoss", "NetIncomeLoss"):
            x = g.get(tax, {}).get(c)
            if x:
                out[f"ejemplo_{tax}_{c}"] = {u: v[-6:] for u, v in x["units"].items()}
    return out


probar("sec_tickers", "https://www.sec.gov/files/company_tickers.json", UA,
       fn=lambda r: {"n": len(r.json()), "primeros": list(r.json().values())[:3]})
probar("sec_aapl", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", UA, fn=resumen_facts)
probar("sec_ggal", "https://data.sec.gov/api/xbrl/companyfacts/CIK0001114700.json", UA, fn=resumen_facts)
probar("sec_ypf", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000904851.json", UA, fn=resumen_facts)
probar("sec_submissions_aapl", "https://data.sec.gov/submissions/CIK0000320193.json", UA,
       fn=lambda r: {k: r.json()["filings"]["recent"][k][:8] for k in ("form", "filingDate", "primaryDocument")})
probar("gnews_aapl", "https://news.google.com/rss/search?q=Apple+AAPL+stock&hl=es-419&gl=AR&ceid=AR:es-419", BROWSER, 2500)
probar("gnews_ggal", "https://news.google.com/rss/search?q=%22Grupo+Financiero+Galicia%22&hl=es-419&gl=AR&ceid=AR:es-419", BROWSER, 2500)
probar("yahoo_rss_aapl", "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US", BROWSER, 2500)
probar("data912_usa", "https://data912.com/live/usa_stocks", BROWSER, fn=lambda r: {"n": len(r.json()), "muestra": r.json()[:3]})
probar("data912_adrs", "https://data912.com/live/usa_adrs", BROWSER, fn=lambda r: {"n": len(r.json()), "muestra": r.json()[:3]})
(OUT / "empresas.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: v.get("status", v.get("error")) for k, v in res.items()})

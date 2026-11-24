"""Relevamiento de fuentes: vuelca respuestas crudas a docs/data/explorar/ para inspeccionarlas.
Corre solo en GitHub Actions (workflow explorar.yml)."""
import json
import warnings
from pathlib import Path

import requests

warnings.filterwarnings("ignore")
OUT = Path("docs/data/explorar")
OUT.mkdir(parents=True, exist_ok=True)
BYMA = "https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free"
H = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}


def guardar(nombre, obj):
    (OUT / f"{nombre}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1)[:200000], encoding="utf-8")


def intento(metodo, url, **kw):
    try:
        r = requests.request(metodo, url, headers=H, timeout=30, verify=False, **kw)
        try:
            body = r.json()
        except Exception:  # noqa: BLE001
            body = r.text[:3000]
        return {"status": r.status_code, "body": body}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


res = {}
for t in ["S30A7", "T15E7", "D15E7", "TZXA7", "AL30", "S26F7"]:
    for body in ({"symbol": t}, {"symbol": f"{t} 24HS"}, {"symbol": t, "Content-Type": "application/json"}):
        r = intento("POST", f"{BYMA}/bnown/fichatecnica/especies/general", json=body)
        res[f"{t}|{json.dumps(body)}"] = r
        if r.get("status") == 200 and r.get("body"):
            break
guardar("byma_ficha", res)

panel_body = {"excludeZeroPxAndQty": True, "T2": False, "T1": True, "T0": False, "page_size": 5000}
r = intento("POST", f"{BYMA}/public-bonds", json=panel_body)
if isinstance(r.get("body"), dict) and "data" in r["body"]:
    r["body"]["data"] = r["body"]["data"][:15]
elif isinstance(r.get("body"), list):
    r["body"] = r["body"][:15]
guardar("byma_public_bonds", r)

bc = {}
for url in ("https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias", "https://api.bcra.gob.ar/estadisticas/v3.0/monetarias"):
    r = intento("GET", url)
    bc[url] = r
guardar("bcra_lista", bc)

hist = intento("GET", "https://data912.com/historical/cedears/SPY")
if isinstance(hist.get("body"), list):
    hist = {"n": len(hist["body"]), "primero": hist["body"][:2], "ultimo": hist["body"][-2:]}
guardar("data912_hist_spy", hist)

ad = {}
for p in ("/finanzas/indices/inflacion", "/finanzas/letras", "/finanzas/lecaps", "/finanzas/bonos-cer",
          "/finanzas/indices/rem", "/finanzas/tasas/plazoFijo"):
    r = intento("GET", "https://api.argentinadatos.com/v1" + p)
    if isinstance(r.get("body"), list):
        r["body"] = r["body"][-3:]
    ad[p] = r
guardar("argentinadatos", ad)
print("listo")

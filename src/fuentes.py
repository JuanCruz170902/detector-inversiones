"""Descarga de datos de mercado. Cada función devuelve datos o lanza excepción;
main.py captura errores por fuente para que una caída no frene todo el informe."""
from __future__ import annotations

import time
import warnings
from datetime import date, timedelta

import requests

DATA912 = "https://data912.com"
ARGDATOS = "https://api.argentinadatos.com/v1"
BCRA = "https://api.bcra.gob.ar/estadisticas"

HEADERS = {"User-Agent": "detector-inversiones (github.com/JuanCruz170902)"}


def _get(url: str, params: dict | None = None, verify: bool = True, intentos: int = 3):
    ultimo_error = None
    for i in range(intentos):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30, verify=verify)
            if r.status_code == 429:
                time.sleep(5 * (i + 1))
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.SSLError as e:
            # el BCRA a veces no envía la cadena intermedia completa
            if verify:
                warnings.filterwarnings("ignore")
                return _get(url, params, verify=False, intentos=intentos)
            ultimo_error = e
        except Exception as e:  # noqa: BLE001
            ultimo_error = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"Fallo {url}: {ultimo_error}")


# ---------------- data912: paneles en vivo e historia ----------------

PANELES = {
    "bonos": "/live/arg_bonds",
    "letras": "/live/arg_notes",
    "ons": "/live/arg_corp",
    "acciones": "/live/arg_stocks",
    "cedears": "/live/arg_cedears",
}


def panel(nombre: str) -> list[dict]:
    return _get(DATA912 + PANELES[nombre])


def mep() -> list[dict]:
    return _get(DATA912 + "/live/mep")


def historia(tipo: str, ticker: str) -> list[dict]:
    """tipo: stocks | cedears | bonds. Devuelve barras diarias {date,o,h,l,c,v}."""
    time.sleep(0.6)  # respetar 120 req/min
    return _get(f"{DATA912}/historical/{tipo}/{ticker}")


# ---------------- ArgentinaDatos: macro y bonos CER ----------------

def bonos_cer() -> dict:
    return _get(ARGDATOS + "/finanzas/bonos-cer")


def inflacion() -> list[dict]:
    return _get(ARGDATOS + "/finanzas/indices/inflacion")


def riesgo_pais() -> dict:
    return _get(ARGDATOS + "/finanzas/indices/riesgo-pais/ultimo")


def dolares() -> list[dict]:
    return _get(ARGDATOS + "/cotizaciones/dolares")


def plazo_fijo() -> list[dict]:
    return _get(ARGDATOS + "/finanzas/tasas/plazoFijo")


# ---------------- BCRA: variables principales ----------------
# ids de la API de Estadísticas Monetarias (v4)
IDS_BCRA = {"a3500": 5, "badlar": 7, "inflacion_mensual": 27, "rem_12m": 29, "cer": 30, "tamar": 44}


def letras() -> dict:
    """LECAP/BONCAP con TNA, TEA, TEM y vencimiento."""
    return _get(ARGDATOS + "/finanzas/letras")


def bcra_principales() -> dict:
    """Último valor de cada variable de IDS_BCRA. Prueba v4 y v3."""
    for url in (f"{BCRA}/v4.0/Monetarias", f"{BCRA}/v3.0/monetarias"):
        try:
            data = _get(url)
            filas = data.get("results", data) if isinstance(data, dict) else data
            por_id = {int(f["idVariable"]): f for f in filas if "idVariable" in f}
            out = {}
            for clave, i in IDS_BCRA.items():
                f = por_id.get(i)
                if f:
                    valor = f.get("ultValorInformado", f.get("valor"))
                    if valor is not None:
                        out[clave] = {"valor": float(valor), "fecha": f.get("ultFechaInformada", f.get("fecha")),
                                      "descripcion": f.get("descripcion")}
            if out:
                return out
        except Exception:  # noqa: BLE001
            continue
    raise RuntimeError("BCRA no respondió")


def bcra_serie(id_variable: int, dias: int = 60) -> list[dict]:
    """Serie diaria [{fecha, valor}] de los últimos `dias`."""
    params = {"desde": hace(dias), "hasta": hoy(), "limit": 3000}
    for url in (f"{BCRA}/v4.0/Monetarias/{id_variable}", f"{BCRA}/v3.0/monetarias/{id_variable}"):
        try:
            data = _get(url, params=params)
            res = data.get("results", []) if isinstance(data, dict) else data
            if res and isinstance(res[0], dict) and "detalle" in res[0]:
                res = res[0]["detalle"]
            filas = [{"fecha": r["fecha"], "valor": float(r["valor"])} for r in res if "fecha" in r]
            if filas:
                return sorted(filas, key=lambda r: r["fecha"])
        except Exception:  # noqa: BLE001
            continue
    raise RuntimeError(f"BCRA serie {id_variable} no respondió")


def hoy() -> str:
    return date.today().isoformat()


def hace(dias: int) -> str:
    return (date.today() - timedelta(days=dias)).isoformat()

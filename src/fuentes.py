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

BUSCAR_BCRA = {
    "a3500": ["tipo de cambio mayorista"],
    "cer": ["cer"],
    "tamar": ["tamar"],
    "badlar": ["badlar"],
    "inflacion_esperada_12m": ["rem", "12 meses"],
}


def bcra_principales() -> dict:
    """Lista de variables monetarias con su último valor. Prueba v4 y v3."""
    for url in (f"{BCRA}/v4.0/Monetarias", f"{BCRA}/v3.0/monetarias"):
        try:
            data = _get(url)
            filas = data.get("results", data) if isinstance(data, dict) else data
            if filas:
                return _mapear_bcra(filas)
        except Exception:  # noqa: BLE001
            continue
    raise RuntimeError("BCRA no respondió")


def _mapear_bcra(filas: list[dict]) -> dict:
    out = {}
    for clave, palabras in BUSCAR_BCRA.items():
        for f in filas:
            desc = str(f.get("descripcion", "")).lower()
            if all(p in desc for p in palabras):
                valor = f.get("valor", f.get("ultValorInformado"))
                fecha = f.get("fecha", f.get("ultFechaInformada"))
                if valor is not None:
                    out[clave] = {"valor": float(valor), "fecha": fecha, "descripcion": f.get("descripcion")}
                    break
    return out


def hoy() -> str:
    return date.today().isoformat()


def hace(dias: int) -> str:
    return (date.today() - timedelta(days=dias)).isoformat()

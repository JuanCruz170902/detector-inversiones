"""Prueba de punta a punta con datos sintéticos (no usa internet).
Correr con: python -m pytest -q  (o python tests/test_offline.py)"""
import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import fuentes as F  # noqa: E402
from src import main as MAIN  # noqa: E402
from src import metricas as M  # noqa: E402
from src import paper  # noqa: E402


def barras(seed, drift):
    random.seed(seed)
    p, out = 100.0, []
    d0 = date.today() - timedelta(days=400)
    for i in range(280):
        p *= 1 + drift + random.gauss(0, 0.015)
        out.append({"date": (d0 + timedelta(days=i)).isoformat(), "o": p, "h": p, "l": p, "c": p, "v": 1e6})
    return out


def falsos(monkeypatch=None):
    def set_(n, f):
        if monkeypatch:
            monkeypatch.setattr(F, n, f)
        else:
            setattr(F, n, f)

    set_("inflacion", lambda: [{"fecha": "2026-09-30", "valor": 2.1}, {"fecha": "2026-10-31", "valor": 2.4}])
    set_("plazo_fijo", lambda: [{"entidad": "X", "tnaClientes": 0.27}, {"entidad": "Y", "tnaClientes": 0.29}])
    set_("dolares", lambda: [{"casa": "oficial", "venta": 1450, "fecha": "2026-11-23"},
                             {"casa": "bolsa", "venta": 1700, "fecha": "2026-11-23"}])
    set_("riesgo_pais", lambda: {"fecha": "2026-11-23", "valor": 620})
    set_("bonos_cer", lambda: {"bonos": [{"ticker": "TZX27", "precioArs": 300, "tirPorcentaje": 6.5},
                                         {"ticker": "TZXM7", "precioArs": 250, "tirPorcentaje": 8.1}]})
    set_("bcra_principales", lambda: {"a3500": {"valor": 1450.0, "fecha": "2026-11-23"}})
    set_("mep", lambda: [{"ticker": "AL30", "mark": 1700}])
    paneles = {
        "bonos": [{"symbol": "AL30", "c": 120000, "v": 9e8, "pct_change": 0.5},
                  {"symbol": "GD30", "c": 122000, "v": 5e8, "pct_change": 0.4},
                  {"symbol": "AL30D", "c": 70, "v": 1e6, "pct_change": 0.1},
                  {"symbol": "TZX27", "c": 30000, "v": 2e8, "pct_change": 0.1},
                  {"symbol": "TZXM7", "c": 25000, "v": 3e8, "pct_change": 0.1}],
        "letras": [{"symbol": "S30A7", "c": 108, "v": 5e8, "pct_change": 0.1},
                   {"symbol": "S29E7", "c": 104, "v": 7e8, "pct_change": 0.1},
                   {"symbol": "D30A7", "c": 101, "v": 1e8, "pct_change": 0.1}],
        "ons": [],
        "acciones": [{"symbol": "GGAL", "c": 7000, "v": 9e9}, {"symbol": "YPFD", "c": 50000, "v": 9e9}],
        "cedears": [{"symbol": "SPY", "c": 40000, "v": 9e9}, {"symbol": "AAPL", "c": 20000, "v": 9e9}],
    }
    set_("panel", lambda n: paneles[n])
    set_("historia", lambda tipo, t: barras(hash(t) % 1000, 0.002 if t in ("SPY", "AAPL", "GGAL") else -0.0005))


def test_punta_a_punta(monkeypatch):
    falsos(monkeypatch)
    res = MAIN.correr(200000, guardar=False)
    for nombre, p in res["perfiles"].items():
        pr = p["propuesta"]
        total = pr["invertido"] + pr["liquidez"] + pr["costos"]
        assert math.isclose(total, 200000, rel_tol=1e-6), (nombre, total)
        assert pr["liquidez"] >= 0
    cons = res["perfiles"]["conservador"]["propuesta"]
    assert not any(p["bucket"] in ("cedears", "acciones_arg") for p in cons["posiciones"])
    # tasa real: 28%/12=2.33 < 2.4 -> negativa -> sube CER
    assert res["perfiles"]["conservador"]["senales"]["tasa_real_negativa"] is True
    est = paper.actualizar({"perfiles": {}}, {n: v["propuesta"] for n, v in res["perfiles"].items()},
                           {"SPY": 41000, "TZXM7": 25500}, 1700, 2.3, hoy="2026-11-24")
    assert est["perfiles"]["conservador"]["historial"][0]["aportado"] == 200000
    print(MAIN.reporte_md(res, est))


def test_vencimientos():
    assert M.vencimiento_desde_ticker("S30A7") == date(2027, 4, 30)
    assert M.clasificar_renta_fija("TZXM7") == "cer"
    assert M.clasificar_renta_fija("D30A7") == "dollar_linked"
    assert M.clasificar_renta_fija("T30J7") == "tasa_fija"


if __name__ == "__main__":
    falsos()
    test_vencimientos()
    res = MAIN.correr(200000, guardar=False)
    print(MAIN.reporte_md(res, {"perfiles": {}}))

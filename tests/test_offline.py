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
    hoy = date.today()
    v = lambda d: (hoy + timedelta(days=d)).isoformat()  # noqa: E731
    set_("bonos_cer", lambda: {"bonos": [
        {"ticker": "TZXM7", "precioArs": 238, "tirPorcentaje": 1.5, "fechaVencimiento": v(120), "volumen": 2e8},
        {"ticker": "TZXA7", "precioArs": 131, "tirPorcentaje": 2.4, "fechaVencimiento": v(150), "volumen": 1e5},
        {"ticker": "TZXY7", "precioArs": 130, "tirPorcentaje": 1.7, "fechaVencimiento": v(185), "volumen": 4e8},
        {"ticker": "TZX28", "precioArs": 362, "tirPorcentaje": 11.6, "fechaVencimiento": v(580), "volumen": 2e8}]})
    set_("letras", lambda: {"letras": [
        {"ticker": "T15E7", "precioArs": 155.4, "teaPorcentaje": 28.7, "temPorcentaje": 2.13, "fechaVencimiento": v(52), "volumenEfectivoArs": 3e10},
        {"ticker": "S26F7", "precioArs": 101.4, "teaPorcentaje": 29.6, "temPorcentaje": 2.19, "fechaVencimiento": v(94), "volumenEfectivoArs": 1e10},
        {"ticker": "T30A7", "precioArs": 139.6, "teaPorcentaje": 31.9, "temPorcentaje": 2.34, "fechaVencimiento": v(157), "volumenEfectivoArs": 2e10},
        {"ticker": "T31Y7", "precioArs": 130.9, "teaPorcentaje": 32.9, "temPorcentaje": 2.40, "fechaVencimiento": v(188), "volumenEfectivoArs": 4e10}]})
    set_("bcra_principales", lambda: {"a3500": {"valor": 1575.0, "fecha": "2026-11-23"},
                                      "rem_12m": {"valor": 24.0, "fecha": "2026-10-31"}})
    set_("bcra_serie", lambda i, d=60: [{"fecha": (hoy - timedelta(days=k)).isoformat(), "valor": 1575 / (1.012 ** (k / 30))} for k in range(45, -1, -1)])
    set_("mep", lambda: [{"ticker": "AL30", "mark": 1700}])
    paneles = {
        "bonos": [{"symbol": "AL30", "c": 120000, "v": 9e8, "pct_change": 0.5},
                  {"symbol": "GD30", "c": 122000, "v": 5e8, "pct_change": 0.4},
                  {"symbol": "AL30D", "c": 62, "v": 1e6, "pct_change": 0.1},
                  {"symbol": "GD30D", "c": 63, "v": 1e6, "pct_change": 0.1},
                  {"symbol": "TZX27", "c": 30000, "v": 2e8, "pct_change": 0.1},
                  {"symbol": "TZXM7", "c": 25000, "v": 3e8, "pct_change": 0.1}],
        "letras": [{"symbol": "S30A7", "c": 108, "v": 5e8, "pct_change": 0.1},
                   {"symbol": "S29E7", "c": 104, "v": 7e8, "pct_change": 0.1},
                   {"symbol": "D30A7", "c": 160500, "v": 1e5, "pct_change": 0.1}],
        "ons": [],
        "acciones": [{"symbol": "GGAL", "c": 7000, "v": 9e9}, {"symbol": "YPFD", "c": 50000, "v": 9e9}],
        "cedears": [{"symbol": "SPY", "c": 40000, "v": 9e9}, {"symbol": "AAPL", "c": 20000, "v": 9e9}],
    }
    set_("panel", lambda n: paneles[n])
    from src import balances as BAL
    if monkeypatch:
        monkeypatch.setattr(BAL, "proximos", lambda dias=7: ({"AAPL": "2026-11-27", "GGAL": "2026-11-26"}, "test"))
    else:
        BAL.proximos = lambda dias=7: ({"AAPL": "2026-11-27", "GGAL": "2026-11-26"}, "test")
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
    sen = res["perfiles"]["conservador"]["senales"]
    assert sen["prefiere"] in ("cer", "tasa_fija", "neutral")
    assert res["curvas"]["breakevens"], "debería haber breakevens"
    hd = {r["ticker"]: r for r in res["curvas"]["hard_dollar"]}
    assert 0 < hd["AL30"]["tir"] < 30, hd["AL30"]
    # balances próximos: AAPL y GGAL no pueden aparecer en ninguna propuesta
    for p in res["perfiles"].values():
        assert not any(x["ticker"] in ("AAPL", "GGAL") for x in p["propuesta"]["posiciones"])
    # TZXA7 no es líquido: no debe elegirse
    assert all(p["ticker"] != "TZXA7" for p in res["perfiles"]["conservador"]["propuesta"]["posiciones"])
    est = paper.actualizar({"perfiles": {}}, {n: v["propuesta"] for n, v in res["perfiles"].items()},
                           {"SPY": 41000, "TZXM7": 25500}, 1700, 2.3, hoy="2026-11-24")
    assert est["perfiles"]["conservador"]["historial"][0]["aportado"] == 200000
    print(MAIN.reporte_md(res, est))


def test_backtest():
    import pandas as pd
    from src import backtest as BT
    ser = {t: pd.Series([b["c"] for b in barras(i, d)], index=pd.to_datetime([b["date"] for b in barras(i, d)]))
           for i, (t, d) in enumerate([("A", 0.002), ("B", 0.001), ("C", -0.001), ("SPY", 0.0008)])}
    cfg = {"peso_ret_3m": 0.5, "peso_ret_6m": 0.5, "penalizar_rsi_mayor_a": 75, "penalizacion_rsi": 0.5}
    r = BT.correr(ser, cfg, {"vol_max_anual": 2}, 2, 0.01, "SPY", min_hist=60)
    assert r and r["meses"] >= 4 and "anual" in r["estrategia"]


def test_hard_dollar_validacion():
    """Flujos contra el pago real del 9-ene-2026 y TIRs contra PPI (liquidación 08/09/2025)."""
    from src import hard_dollar as HD
    d = date(2026, 1, 9)
    pagos = {"AL29": (0.40, 10.0), "AL30": (0.30, 8.0), "AL35": (2.0625, 0), "AE38": (2.50, 0), "AL41": (1.75, 0),
             "GD46": (1.97, 2.27)}
    for t, (renta, amort) in pagos.items():
        a = HD.BONOS[HD._serie(t)]["amort"].get(d, 0)
        total = dict(HD.flujos(t))[d]
        assert abs(a - amort) < 0.01 and abs(total - a - renta) < 0.01, t
    ppi = {"GD29": (58.33, 19.0), "GD30": (55.30, 18.2), "GD35": (57.29, 15.1), "GD38": (61.33, 15.6),
           "GD41": (53.88, 14.6), "GD46": (53.66, 14.5), "AL30": (52.40, 21.1)}
    for t, (sucio, y) in ppi.items():
        assert abs(HD.tir(t, sucio, date(2025, 9, 8))["tir"] - y) < 0.6, t


def test_splits():
    import pandas as pd
    s = pd.Series([100, 101, 102, 10.3, 10.4], index=pd.date_range("2026-01-01", periods=5))
    a = M.ajustar_splits(s)
    assert abs(a.iloc[2] - a.iloc[3]) < 1e-9 and a.pct_change().min() > -0.05


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


def test_prueba_semanal(monkeypatch, tmp_path):
    from datetime import datetime
    from src import prueba as P
    falsos(monkeypatch)
    monkeypatch.setattr(P, "RUTA", tmp_path / "prueba.json")
    monkeypatch.setattr(P, "ahora_art", lambda: datetime(2026, 11, 25, 11, 40, tzinfo=P.ART))
    est = P.entrar()
    # con el precio de venta 1% arriba del último, no debe perder unidades si el presupuesto alcanza
    for n, c in est["carteras"].items():
        gastado = sum(p["monto"] + p["costo_compra"] for p in c["posiciones"])
        assert abs(gastado + c["liquidez_inicial"] - 200000) < 1, n
        assert c["liquidez_inicial"] >= 0
    monkeypatch.setattr(P, "ahora_art", lambda: datetime(2026, 11, 26, 17, 50, tzinfo=P.ART))
    est = P.valuar()
    d = est["dias"][-1]
    assert d["fecha"] == "2026-11-26" and set(d["perfiles"]) == {"conservador", "moderado", "riesgoso"}
    # sin cambio de precios el valor es el aporte menos costos de compra y venta, más la caución
    for v in d["perfiles"].values():
        assert 0.97 < v["valor"] / 200000 < 1.01
    assert P.entrar()["entrada"] == est["entrada"]  # no re-entra
    assert P.entrar(forzar=True)["entrada"] == est["entrada"]  # --forzar no pisa una entrada en vivo
    # una valuación de madrugada corresponde a la rueda anterior
    monkeypatch.setattr(P, "ahora_art", lambda: datetime(2026, 11, 27, 0, 46, tzinfo=P.ART))
    assert P.valuar()["dias"][-1]["fecha"] == "2026-11-26"

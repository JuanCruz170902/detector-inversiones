"""Prueba semanal: $200.000 por perfil, invertidos a la apertura siguiendo al detector, valuados cada cierre.

    python -m src.prueba entrar     # una sola vez, con precios en vivo (punta vendedora + comisiones)
    python -m src.prueba valuar     # cada cierre: valor de liquidación (punta compradora − comisión de venta)

Benchmarks: los mismos $200.000 en dólar MEP y en plazo fijo (TNA promedio de bancos).
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime, timedelta, timezone

from . import fuentes as F
from . import main as MAIN
from . import motor

RUTA = MAIN.SALIDA / "prueba_semanal.json"
ART = timezone(timedelta(hours=-3))
INICIO = date(2026, 11, 25)
FIN = date(2026, 12, 1)          # 5 ruedas: 25, 26, 27 y 30 de noviembre, 1 de diciembre
MONTO = 200000
ES_BONO = motor.BUCKETS_BONO


def ahora_art() -> datetime:
    return datetime.now(ART)


def precios_vivos() -> dict[str, dict]:
    """ticker -> {ultimo, bid, ask, volumen} de todos los paneles de data912."""
    out = {}
    for nombre in F.PANELES:
        try:
            for f in F.panel(nombre):
                t = f.get("symbol")
                if not t:
                    continue
                out[t] = {"ultimo": _f(f.get("c")), "bid": _f(f.get("px_bid")), "ask": _f(f.get("px_ask")),
                          "volumen": _f(f.get("v"))}
        except Exception as e:  # noqa: BLE001
            print("panel", nombre, e)
    return out


def _f(x):
    try:
        x = float(x)
        return x if x > 0 and not math.isnan(x) else None
    except (TypeError, ValueError):
        return None


def mep_actual() -> float | None:
    try:
        casas = MAIN.ultimo_por_casa(F.dolares())
        return float(casas["bolsa"]["venta"])
    except Exception:  # noqa: BLE001
        return None


def cargar() -> dict:
    return json.loads(RUTA.read_text(encoding="utf-8")) if RUTA.exists() else {}


def guardar(est: dict):
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    RUTA.write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")


def entrar(forzar: bool = False, tardia: bool = False, rehacer: bool = False) -> dict:
    est = cargar()
    if est.get("entrada") and not rehacer and not (forzar and est["entrada"].get("tardia")):
        # --forzar solo reemplaza una entrada de respaldo; una entrada en vivo no se pisa nunca
        print("La prueba ya tiene entrada:", est["entrada"]["fecha_hora"])
        return est
    perfiles, _ = MAIN.cargar_config()
    broker = perfiles["broker"]
    res = MAIN.correr(MONTO, guardar=False)            # el detector elige con los datos de este momento
    px = precios_vivos()
    mep = res["macro"].get("dolar_mep") or mep_actual()
    tna = res["macro"].get("tna_plazo_fijo")
    carteras = {}
    for nombre, p in res["perfiles"].items():
        posiciones, gastado = [], 0.0
        for pos in p["propuesta"]["posiciones"]:
            t = pos.get("ticker")
            if pos["bucket"] == "liquidez" or not pos.get("cantidad"):
                continue
            es_bono = pos["bucket"] in ES_BONO
            q = px.get(t, {})
            precio = q.get("ask") or q.get("ultimo") or pos["precio"]   # se compra en la punta vendedora
            unit = precio / 100 if es_bono else precio
            # presupuesto = lo asignado a esa posición (no lo que gastó la propuesta con otro precio)
            presupuesto = max(pos.get("monto") or 0, pos["monto_bruto"] + pos["costo"])
            costo_pct = motor.costo_operacion(1, es_bono, broker)
            cant = math.floor(presupuesto / (unit * (1 + costo_pct)))
            if cant <= 0:
                continue
            bruto = cant * unit
            costo = motor.costo_operacion(bruto, es_bono, broker)
            gastado += bruto + costo
            posiciones.append({"ticker": t, "bucket": pos["bucket"], "cantidad": cant, "precio_entrada": precio,
                               "fuente_precio": "ask" if q.get("ask") else ("ultimo" if q.get("ultimo") else "detector"),
                               "monto": round(bruto, 2), "costo_compra": round(costo, 2),
                               "tir_entrada": pos.get("tir"), "vencimiento": pos.get("vencimiento")})
        carteras[nombre] = {"posiciones": posiciones, "liquidez_inicial": round(MONTO - gastado, 2),
                            "senales": p["senales"]["notas"], "buckets": p["propuesta"]["buckets"]}
    est = {"inicio": INICIO.isoformat(), "fin": FIN.isoformat(), "monto": MONTO,
           "entrada": {"fecha_hora": ahora_art().isoformat(timespec="minutes"), "mep": mep, "tna_plazo_fijo": tna,
                       "tardia": tardia, "nota": "precios de cierre (la entrada a la apertura no corrió)" if tardia else
                       "precios en vivo, punta vendedora"},
           "carteras": carteras, "dias": [],
           "historial_entradas": (est.get("historial_entradas", []) + [est["entrada"]]) if est.get("entrada") else []}
    guardar(est)
    print(json.dumps(est, ensure_ascii=False, indent=1)[:3000])
    return est


def fecha_rueda(t: datetime) -> date:
    """Rueda a la que corresponde una valuación: antes de la apertura (11:00) es la rueda hábil anterior."""
    d = t.date()
    if t.hour < 11:
        d -= timedelta(days=1)
        while d.weekday() >= 5:
            d -= timedelta(days=1)
    return d


def valuar() -> dict | None:
    est = cargar()
    t = ahora_art()
    hoy = fecha_rueda(t)
    if not est.get("entrada"):
        if INICIO <= hoy <= FIN and t.hour >= 11:   # nunca entra antes de la apertura
            est = entrar(tardia=True)           # respaldo: si el cron de la apertura falló, entra al cierre
        else:
            print("Prueba sin iniciar")
            return None
    if hoy > date.fromisoformat(est["fin"]) + timedelta(days=3):
        print("Prueba terminada")
        return est
    perfiles, _ = MAIN.cargar_config()
    broker = perfiles["broker"]
    px = precios_vivos()
    mep = mep_actual()
    ent = est["entrada"]
    dias_corridos = max((hoy - date.fromisoformat(ent["fecha_hora"][:10])).days, 0)
    if hoy < date.fromisoformat(ent["fecha_hora"][:10]):
        print("Valuación anterior a la entrada: se omite")
        return est
    tna_liq = (ent.get("tna_plazo_fijo") or 0) / 100
    fila = {"fecha": hoy.isoformat(), "hora": "17:00" if t.hour < 11 or t.hour >= 17 else t.strftime("%H:%M"),
            "valuado": t.isoformat(timespec="minutes"), "perfiles": {}}
    for nombre, c in est["carteras"].items():
        valor = c["liquidez_inicial"] * (1 + tna_liq * dias_corridos / 365)   # caución / FCI MM
        detalle = []
        for pos in c["posiciones"]:
            es_bono = pos["bucket"] in ES_BONO
            q = px.get(pos["ticker"], {})
            precio = q.get("bid") or q.get("ultimo") or pos.get("ultimo_precio") or pos["precio_entrada"]
            pos["ultimo_precio"] = precio
            unit = precio / 100 if es_bono else precio
            bruto = pos["cantidad"] * unit
            neto = bruto - motor.costo_operacion(bruto, es_bono, broker)     # si vendiera hoy
            valor += neto
            detalle.append({"ticker": pos["ticker"], "precio": precio, "valor_neto": round(neto, 2),
                            "resultado": round(neto - pos["monto"] - pos["costo_compra"], 2),
                            "var_precio": round(precio / pos["precio_entrada"] - 1, 4)})
        fila["perfiles"][nombre] = {"valor": round(valor, 2), "rend": round(valor / est["monto"] - 1, 5), "detalle": detalle}
    fila["bench"] = {
        "mep": round(est["monto"] / ent["mep"] * mep, 2) if mep and ent.get("mep") else None,
        "plazo_fijo": round(est["monto"] * (1 + tna_liq * dias_corridos / 365), 2),
        "mep_valor": mep,
    }
    est["dias"] = [d for d in est["dias"] if d["fecha"] != fila["fecha"]] + [fila]
    guardar(est)
    print(json.dumps(fila, ensure_ascii=False, indent=1))
    return est


if __name__ == "__main__":
    accion = sys.argv[1] if len(sys.argv) > 1 else "valuar"
    if accion == "entrar":
        hoy = ahora_art().date()
        if hoy < INICIO and "--forzar" not in sys.argv:
            print("Todavía no empieza la prueba")
        else:
            entrar(forzar="--forzar" in sys.argv, rehacer="--rehacer" in sys.argv)
    else:
        valuar()

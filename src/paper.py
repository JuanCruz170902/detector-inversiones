"""Paper trading: simula invertir el monto mensual en cada perfil siguiendo la propuesta del día,
y valúa la cartera todos los días. Benchmarks: mismos aportes en dólar MEP y ajustados por inflación."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ES_BONO = {"cer", "tasa_fija", "dollar_linked", "tamar", "hard_dollar"}


def cargar(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"inicio": date.today().isoformat(), "perfiles": {}}


def actualizar(estado: dict, propuestas: dict, precios: dict[str, float], mep: float | None,
               tasa_liquidez_mensual: float, hoy: str | None = None) -> dict:
    """precios: ticker -> precio de pantalla (bonos cada 100 VN)."""
    hoy = hoy or date.today().isoformat()
    mes = hoy[:7]
    for nombre, prop in propuestas.items():
        p = estado["perfiles"].setdefault(nombre, {"posiciones": {}, "liquidez": 0.0, "aportes": [],
                                                   "historial": [], "ultimo_precio": {}})
        # liquidez rinde caución/FCI MM (aprox. diaria)
        if p["historial"] and p["historial"][-1]["fecha"] < hoy:
            dias = (date.fromisoformat(hoy) - date.fromisoformat(p["historial"][-1]["fecha"])).days
            p["liquidez"] *= (1 + tasa_liquidez_mensual / 100) ** (dias / 30)
        # aporte mensual: primer día con datos de cada mes
        if not any(a["mes"] == mes for a in p["aportes"]):
            for pos in prop["posiciones"]:
                t = pos.get("ticker")
                if pos["bucket"] == "liquidez" or not pos.get("cantidad"):
                    continue
                d = p["posiciones"].setdefault(t, {"cantidad": 0, "bucket": pos["bucket"]})
                d["cantidad"] += pos["cantidad"]
            p["liquidez"] += prop["liquidez"]
            p["aportes"].append({"mes": mes, "fecha": hoy, "monto": prop["monto"], "mep": mep,
                                 "costos": prop["costos"]})
        # valuación
        valor = p["liquidez"]
        for t, d in p["posiciones"].items():
            px = precios.get(t) or p["ultimo_precio"].get(t)
            if px:
                p["ultimo_precio"][t] = px
                valor += d["cantidad"] * (px / 100 if d["bucket"] in ES_BONO else px)
        aportado = sum(a["monto"] for a in p["aportes"])
        bench_usd = sum(a["monto"] / a["mep"] for a in p["aportes"] if a.get("mep")) * mep if mep else None
        registro = {"fecha": hoy, "valor": round(valor, 2), "aportado": aportado,
                    "rend": round(valor / aportado - 1, 4) if aportado else 0,
                    "bench_mep": round(bench_usd, 2) if bench_usd else None}
        p["historial"] = [h for h in p["historial"] if h["fecha"] != hoy] + [registro]
    return estado

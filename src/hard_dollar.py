"""TIR en dólares de los soberanos del canje 2020 (Bonares AL/AE ley local y Globales GD ley NY).

Condiciones por cada 100 VN originales; pagos el 9-ene y 9-jul. Cupón step-up anual sobre valor residual:
el tramo indicado rige para los pagos HASTA esa fecha inclusive.

Verificación (tests/test_offline.py::test_hard_dollar_validacion):
- Pago del 9-ene-2026 (iProfesional, 07/01/2026): AL29/GD29 0,40% renta + 10 amort; AL30/GD30 0,30% + 8;
  AL35/GD35 2,06%; AE38/GD38 2,50%; AL41/GD41 1,75%; GD46 1,97% + 2,27 amort.  → coinciden.
- TIRs publicadas por PPI al 08/09/2025 → coinciden con tolerancia de ±0,6 pp.

Supuesto: el precio de pantalla (especie "D", USD MEP) se toma como precio sucio (incluye cupón corrido).
"""
from __future__ import annotations

from datetime import date

# (fecha hasta la que rige, tasa anual)
STEP_30 = [(date(2021, 7, 9), 0.00125), (date(2023, 7, 9), 0.005), (date(2027, 7, 9), 0.0075), (date(2030, 7, 9), 0.0175)]
STEP_35 = [(date(2021, 7, 9), 0.00125), (date(2022, 7, 9), 0.01125), (date(2023, 7, 9), 0.015), (date(2024, 7, 9), 0.03625),
           (date(2027, 7, 9), 0.04125), (date(2028, 7, 9), 0.0475), (date(2035, 7, 9), 0.05)]
STEP_38 = [(date(2021, 7, 9), 0.00125), (date(2022, 7, 9), 0.02), (date(2023, 7, 9), 0.03875), (date(2024, 7, 9), 0.0425),
           (date(2038, 1, 9), 0.05)]
STEP_41 = [(date(2021, 7, 9), 0.00125), (date(2022, 7, 9), 0.025), (date(2029, 7, 9), 0.035), (date(2041, 7, 9), 0.04875)]
STEP_46 = [(date(2021, 7, 9), 0.00125), (date(2022, 7, 9), 0.01125), (date(2023, 7, 9), 0.015), (date(2024, 7, 9), 0.03625),
           (date(2027, 7, 9), 0.04125), (date(2028, 7, 9), 0.04375), (date(2046, 7, 9), 0.05)]


def _fechas(desde: date, hasta: date):
    y = desde.year
    while True:
        for d in (date(y, 1, 9), date(y, 7, 9)):
            if desde <= d <= hasta:
                yield d
        if date(y, 12, 31) >= hasta:
            return
        y += 1


def _cuotas(primera: date, ultima: date, n_esperado: int, extra: dict | None = None) -> dict:
    fechas = list(_fechas(primera, ultima))
    assert len(fechas) == n_esperado, (primera, ultima, len(fechas))
    resto = 100.0 - sum((extra or {}).values())
    return {**(extra or {}), **{d: resto / len(fechas) for d in fechas}}


BONOS = {
    "29": {"step": [(date(2029, 7, 9), 0.01)], "amort": _cuotas(date(2025, 1, 9), date(2029, 7, 9), 10), "vto": date(2029, 7, 9)},
    "30": {"step": STEP_30, "amort": _cuotas(date(2025, 1, 9), date(2030, 7, 9), 12, {date(2024, 7, 9): 4.0}), "vto": date(2030, 7, 9)},
    "35": {"step": STEP_35, "amort": _cuotas(date(2031, 1, 9), date(2035, 7, 9), 10), "vto": date(2035, 7, 9)},
    "38": {"step": STEP_38, "amort": _cuotas(date(2027, 7, 9), date(2038, 1, 9), 22), "vto": date(2038, 1, 9)},
    "41": {"step": STEP_41, "amort": _cuotas(date(2028, 1, 9), date(2041, 7, 9), 28), "vto": date(2041, 7, 9)},
    "46": {"step": STEP_46, "amort": _cuotas(date(2025, 1, 9), date(2046, 7, 9), 44), "vto": date(2046, 7, 9)},
}


def _serie(ticker: str) -> str | None:
    base = ticker.upper()
    if base.endswith(("D", "C")) and len(base) == 5:
        base = base[:4]
    if base[:2] in ("AL", "GD", "AE") and base[2:] in BONOS:
        return base[2:]
    return None


def _tasa(step, d: date) -> float:
    for hasta, t in step:
        if d <= hasta:
            return t
    return step[-1][1]


def flujos(ticker: str) -> list[tuple[date, float]]:
    """Flujos (cupón + amortización) por 100 VN originales, desde el primer pago (ene-2021)."""
    s = _serie(ticker)
    if not s:
        return []
    b = BONOS[s]
    residual, out = 100.0, []
    for d in _fechas(date(2021, 1, 9), b["vto"]):
        if residual <= 1e-9:
            break
        cupon = residual * _tasa(b["step"], d) / 2
        a = b["amort"].get(d, 0.0)
        out.append((d, cupon + a))
        residual -= a
    return out


def residual(ticker: str, hoy: date) -> float:
    s = _serie(ticker)
    return 100.0 - sum(a for d, a in BONOS[s]["amort"].items() if d <= hoy) if s else float("nan")


def tir(ticker: str, precio_usd: float, hoy: date | None = None) -> dict | None:
    hoy = hoy or date.today()
    fl = [(d, f) for d, f in flujos(ticker) if d > hoy]
    if not fl or not precio_usd or precio_usd <= 0:
        return None

    def vpn(r):
        return sum(f / (1 + r) ** ((d - hoy).days / 365) for d, f in fl) - precio_usd

    lo, hi = -0.5, 2.0
    if vpn(lo) * vpn(hi) > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if vpn(lo) * vpn(mid) <= 0:
            hi = mid
        else:
            lo = mid
    r = (lo + hi) / 2
    dur = sum((d - hoy).days / 365 * f / (1 + r) ** ((d - hoy).days / 365) for d, f in fl) / precio_usd
    res = residual(ticker, hoy)
    return {"tir": round(r * 100, 2), "duration": round(dur, 2), "md": round(dur / (1 + r), 2),
            "residual": round(res, 2), "paridad": round(precio_usd / res * 100, 1) if res else None,
            "proximo_pago": fl[0][0].isoformat(), "monto_proximo_pago": round(fl[0][1], 4)}

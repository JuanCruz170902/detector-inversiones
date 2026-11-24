"""TIR en dólares de los soberanos cortos (AL29/GD29, AL30/GD30).

Flujos según las condiciones de emisión del canje 2020 (por cada 100 VN originales):
- AL29/GD29: cupón 1% anual; amortiza 10 cuotas semestrales iguales de 10 (9-ene / 9-jul, 2025 a 2029).
- AL30/GD30: amortiza 4 el 9-jul-2024 y 12 cuotas de 8 (9-ene / 9-jul, 2025 a 2030);
  cupón step-up 0,125% → 0,50% (desde jul-21) → 0,75% (desde jul-23) → 1,75% (desde jul-27).
Verificar contra el prospecto antes de usar con dinero real. Los precios en USD vienen de la especie "D" (MEP).
"""
from __future__ import annotations

from datetime import date


def _fechas(desde: int, hasta: int):
    for y in range(desde, hasta + 1):
        yield date(y, 1, 9)
        yield date(y, 7, 9)


def flujos(ticker: str) -> list[tuple[date, float]]:
    base = ticker.upper().rstrip("D")
    if base in ("AL29", "GD29"):
        amort = {d: 10.0 for d in _fechas(2025, 2029)}
        def tasa(_d): return 0.01
        inicio = 2021
    elif base in ("AL30", "GD30"):
        amort = {date(2024, 7, 9): 4.0, **{d: 8.0 for d in _fechas(2025, 2030)}}
        def tasa(d):
            if d <= date(2021, 7, 9):
                return 0.00125
            if d <= date(2023, 7, 9):
                return 0.005
            if d <= date(2027, 7, 9):
                return 0.0075
            return 0.0175
        inicio = 2021
    else:
        return []
    residual, out = 100.0, []
    for d in _fechas(inicio, 2030):
        if residual <= 1e-9:
            break
        cupon = residual * tasa(d) / 2
        a = amort.get(d, 0.0)
        out.append((d, cupon + a))
        residual -= a
    return out


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
    valor_residual = sum(f for _, f in fl)
    return {"tir": round(r * 100, 2), "duration": round(dur, 2), "flujos_restantes": round(valor_residual, 2),
            "proximo_pago": fl[0][0].isoformat()}

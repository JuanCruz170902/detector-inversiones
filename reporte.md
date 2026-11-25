# Detector de oportunidades — 2026-11-25

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.46
- Dólar oficial: 1615.0
- Dólar MEP: 1695.1
- Dólar CCL: 1797.1
- Riesgo país (pb): 1094.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 3.46

## Curva en pesos: inflación implícita

| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |
|---|---|---|---|---|
| T15E7 | 28.95% | X29E7 | -0.1% | 2.15% |
| S29E7 | 28.82% | X29E7 | -0.1% | 2.14% |
| S26F7 | 30.45% | X29E7 | -0.1% | 2.25% |
| T30A7 | 33.35% | TZXA7 | 3.44% | 2.14% |
| T31Y7 | 34.12% | TZXY7 | 3.26% | 2.2% |
| T30J7 | 33.6% | TZX27 | 3.27% | 2.17% |
| TY30P | 32.41% | TXMJ0 | 8.28% | 1.69% |

## Soberanos en dólares

- AL30: TIR 20.43% · duration 1.62 · paridad 74.5% · precio USD 47.67
- AL29: TIR 18.32% · duration 1.24 · paridad 81.7% · precio USD 49.021
- GD30: TIR 17.98% · duration 1.65 · paridad 77.0% · precio USD 49.302
- AE38: TIR 17.59% · duration 3.85 · paridad 62.4% · precio USD 62.38
- GD29: TIR 16.71% · duration 1.25 · paridad 83.1% · precio USD 49.868
- AL35: TIR 16.18% · duration 4.97 · paridad 59.7% · precio USD 59.65
- AL41: TIR 15.98% · duration 5.0 · paridad 55.5% · precio USD 55.49
- GD38: TIR 14.82% · duration 4.06 · paridad 68.5% · precio USD 68.54
- GD35: TIR 14.62% · duration 5.04 · paridad 63.8% · precio USD 63.82
- GD46: TIR 14.45% · duration 5.24 · paridad 58.9% · precio USD 53.55
- GD41: TIR 14.27% · duration 5.2 · paridad 59.9% · precio USD 59.86

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.30% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57350 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.948 | $ 154 |
| cer | TZXA7 | 30489 VN | $ 39.895 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 20.899 | $ 0 |

Paper trading: valor $ 200.242 sobre $ 200.000 aportados (+0.12%); mismos aportes en MEP: $ 194.493.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.30% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 43012 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 50 VN | $ 39.710 | $ 104 |
| cedears_etf | SPY | 1 acciones | $ 20.650 | $ 129 |
| cedears_etf | EEM | 1 acciones | $ 19.290 | $ 120 |
| cer | TZXA7 | 15244 VN | $ 19.947 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 39.999 | $ 0 |

Paper trading: valor $ 198.438 sobre $ 200.000 aportados (-0.78%); mismos aportes en MEP: $ 194.493.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.30% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.160 | $ 176 |
| cedears | WMT | 2 acciones | $ 25.840 | $ 161 |
| cedears | PBR | 1 acciones | $ 27.920 | $ 174 |
| tasa_fija | T30A7 | 21506 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 22.088 | $ 138 |
| acciones_arg | YPFD | 4 acciones | $ 21.860 | $ 137 |
| liquidez | CAUCION/FCI MM |  | $ 43.347 | $ 0 |

Paper trading: valor $ 195.888 sobre $ 200.000 aportados (-2.06%); mismos aportes en MEP: $ 194.493.

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +44.8% | +49.1% (SPY) | -17.6% |
| riesgoso_cedears | 2023-02-28 a 2026-11-30 | +81.6% | +75.4% (SPY) | -17.6% |
| riesgoso_acciones_arg | 2022-12-31 a 2026-11-30 | +35.4% | +88.7% (igual peso del universo) | -57.3% |

### Variantes de la regla

| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |
|---|---|---|---|---|---|---|---|
| moderado_cedears_etf | actual (12m) | +44.8% | 22.8% | -17.6% | 1.96 | +49.1% | 1.68 |
| moderado_cedears_etf | v0.1 (3m+6m / vol, RSI) | +32.8% | 21.9% | -27.4% | 1.5 | +49.1% | 1.68 |
| moderado_cedears_etf | 6m+12m / vol | +41.1% | 22.1% | -18.9% | 1.86 | +49.1% | 1.68 |
| moderado_cedears_etf | actual, top 5 | +59.9% | 20.0% | -13.6% | 2.99 | +75.4% | 2.25 |
| moderado_cedears_etf | actual, sin filtros | +44.2% | 24.4% | -16.3% | 1.81 | +49.1% | 1.68 |
| riesgoso_cedears | actual (12m) | +81.6% | 45.6% | -17.6% | 1.79 | +75.4% | 2.25 |
| riesgoso_cedears | v0.1 (3m+6m / vol, RSI) | +41.9% | 39.6% | -25.8% | 1.06 | +75.4% | 2.25 |
| riesgoso_cedears | 6m+12m / vol | +64.1% | 34.2% | -15.8% | 1.87 | +75.4% | 2.25 |
| riesgoso_cedears | actual, top 5 | +76.7% | 44.6% | -15.4% | 1.72 | +75.4% | 2.25 |
| riesgoso_cedears | actual, sin filtros | +82.3% | 46.0% | -17.6% | 1.79 | +75.4% | 2.25 |
| riesgoso_acciones_arg | actual (12m) | +35.4% | 63.4% | -57.3% | 0.56 | +88.7% | 1.41 |
| riesgoso_acciones_arg | v0.1 (3m+6m / vol, RSI) | +18.2% | 51.8% | -65.0% | 0.35 | +88.7% | 1.41 |
| riesgoso_acciones_arg | 6m+12m / vol | +39.4% | 53.6% | -56.7% | 0.74 | +88.7% | 1.41 |
| riesgoso_acciones_arg | actual, top 5 | +47.3% | 56.8% | -59.1% | 0.83 | +88.7% | 1.41 |
| riesgoso_acciones_arg | actual, sin filtros | +37.6% | 57.8% | -58.2% | 0.65 | +88.7% | 1.41 |

## Estado de fuentes

- argdatos_inflacion: ok
- argdatos_plazo_fijo: ok
- argdatos_dolares: ok
- argdatos_riesgo_pais: ok
- argdatos_bonos_cer: ok
- argdatos_letras: ok
- bcra_a3500_serie: ok
- bcra: ok
- data912_mep: ok
- calendario_balances: ok (nasdaq, 175 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- bcra_badlar_serie: ok

# Detector de oportunidades — 2026-11-25

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.47
- Dólar oficial: 1600.0
- Dólar MEP: 1743.1
- Dólar CCL: 1806.2
- Riesgo país (pb): 1035.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 3.46

## Curva en pesos: inflación implícita

| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |
|---|---|---|---|---|
| S26F7 | 29.64% | TZXM7 | 1.54% | 2.06% |
| T30A7 | 31.95% | TZXM7 | 1.54% | 2.21% |
| T31Y7 | 32.92% | TZXY7 | 1.66% | 2.26% |
| T30J7 | 32.41% | TZXY7 | 1.66% | 2.23% |
| TY30P | 32.03% | TXMJ0 | 8.13% | 1.68% |

## Soberanos en dólares

- AL30: TIR 20.61% · duration 1.62 · paridad 74.3% · precio USD 47.55
- GD30: TIR 18.12% · duration 1.65 · paridad 76.9% · precio USD 49.2
- AL29: TIR 17.41% · duration 1.25 · paridad 82.5% · precio USD 49.5
- GD29: TIR 15.97% · duration 1.26 · paridad 83.8% · precio USD 50.27
- AE38: TIR 17.4% · duration 3.87 · paridad 62.8% · precio USD 62.78
- AL35: TIR 16.15% · duration 4.97 · paridad 59.7% · precio USD 59.71
- AL41: TIR 15.7% · duration 5.03 · paridad 56.2% · precio USD 56.16
- GD38: TIR 14.78% · duration 4.06 · paridad 68.7% · precio USD 68.65
- GD35: TIR 14.52% · duration 5.04 · paridad 64.1% · precio USD 64.1
- GD41: TIR 13.75% · duration 5.26 · paridad 61.3% · precio USD 61.28
- GD46: TIR 13.22% · duration 5.47 · paridad 62.4% · precio USD 56.74

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.07% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57136 VN | $ 79.790 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.590 | $ 153 |
| cer | TZXM7 | 16755 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.260 | $ 0 |

Paper trading: valor $ 199.680 sobre $ 200.000 aportados (-0.16%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.07% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42852 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 49 VN | $ 39.391 | $ 103 |
| cedears_etf | SPY | 1 acciones | $ 21.550 | $ 135 |
| cedears_etf | EEM | 1 acciones | $ 20.450 | $ 128 |
| cer | TZXM7 | 8377 VN | $ 19.946 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 38.246 | $ 0 |

Paper trading: valor $ 200.909 sobre $ 200.000 aportados (+0.45%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.07% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.420 | $ 177 |
| cedears | WMT | 2 acciones | $ 26.240 | $ 164 |
| cedears | PBR | 1 acciones | $ 28.100 | $ 175 |
| tasa_fija | T30A7 | 21426 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 23.088 | $ 144 |
| acciones_arg | YPFD | 4 acciones | $ 22.940 | $ 143 |
| liquidez | CAUCION/FCI MM |  | $ 40.409 | $ 0 |

Paper trading: valor $ 198.277 sobre $ 200.000 aportados (-0.86%); mismos aportes en MEP: $ 200.000.

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
- calendario_balances: ok (nasdaq, 171 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- bcra_badlar_serie: ok

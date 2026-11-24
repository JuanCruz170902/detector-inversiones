# Detector de oportunidades — 2026-11-24

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.47
- Dólar oficial: 1600.0
- Dólar MEP: 1743.1
- Dólar CCL: 1806.2
- Riesgo país (pb): 1035.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 2.77

## Curva en pesos: inflación implícita

| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |
|---|---|---|---|---|
| S26F7 | 29.64% | TZXM7 | 1.54% | 2.06% |
| T30A7 | 31.95% | TZXM7 | 1.54% | 2.21% |
| T31Y7 | 32.92% | TZXY7 | 1.66% | 2.26% |
| T30J7 | 32.41% | TZXY7 | 1.66% | 2.23% |
| TY30P | 32.03% | TXMJ0 | 8.13% | 1.68% |

## Soberanos en dólares

- AL30: TIR 20.67% · duration 1.62 · precio USD 47.488
- AL29: TIR 18.11% · duration 1.25 · precio USD 49.109
- GD30: TIR 17.94% · duration 1.65 · precio USD 49.305
- GD29: TIR 15.71% · duration 1.26 · precio USD 50.39

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.40% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57136 VN | $ 79.790 | $ 209 |
| dollar_linked | D31M7 | 37 VN | $ 58.312 | $ 152 |
| cer | TZXM7 | 16755 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.538 | $ 0 |

Paper trading: valor $ 199.613 sobre $ 200.000 aportados (-0.19%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.40% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42852 VN | $ 59.843 | $ 156 |
| cedears_etf | IWM | 1 acciones | $ 47.900 | $ 299 |
| hard_dollar | AL30 | 49 VN | $ 39.298 | $ 103 |
| cer | TZXM7 | 8377 VN | $ 19.946 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 32.403 | $ 0 |

Paper trading: valor $ 200.262 sobre $ 200.000 aportados (+0.13%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.40% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.520 | $ 178 |
| cedears | PBR | 1 acciones | $ 28.740 | $ 179 |
| cedears | WMT | 2 acciones | $ 26.260 | $ 164 |
| tasa_fija | T30A7 | 21426 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 23.562 | $ 147 |
| acciones_arg | BMA | 2 acciones | $ 18.440 | $ 115 |
| liquidez | CAUCION/FCI MM |  | $ 43.694 | $ 0 |

Paper trading: valor $ 199.181 sobre $ 200.000 aportados (-0.41%); mismos aportes en MEP: $ 200.000.

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +42.2% | +47.3% (SPY) | -17.6% |
| riesgoso_cedears | 2023-02-28 a 2026-11-30 | +82.3% | +73.6% (SPY) | -17.6% |
| riesgoso_acciones_arg | 2022-12-31 a 2026-11-30 | +34.8% | +88.0% (igual peso del universo) | -58.0% |

### Variantes de la regla

| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |
|---|---|---|---|---|---|---|---|
| moderado_cedears_etf | actual (12m) | +42.2% | 23.2% | -17.6% | 1.82 | +47.3% | 1.62 |
| moderado_cedears_etf | v0.1 (3m+6m / vol, RSI) | +31.2% | 22.0% | -27.4% | 1.42 | +47.3% | 1.62 |
| moderado_cedears_etf | 6m+12m / vol | +39.3% | 22.2% | -18.9% | 1.77 | +47.3% | 1.62 |
| moderado_cedears_etf | actual, top 5 | +57.8% | 20.3% | -13.6% | 2.85 | +73.6% | 2.19 |
| moderado_cedears_etf | actual, sin filtros | +41.7% | 24.8% | -16.3% | 1.68 | +47.3% | 1.62 |
| riesgoso_cedears | actual (12m) | +82.3% | 45.5% | -17.6% | 1.81 | +73.6% | 2.19 |
| riesgoso_cedears | v0.1 (3m+6m / vol, RSI) | +41.1% | 39.6% | -25.8% | 1.04 | +73.6% | 2.19 |
| riesgoso_cedears | 6m+12m / vol | +63.5% | 34.2% | -15.8% | 1.85 | +73.6% | 2.19 |
| riesgoso_cedears | actual, top 5 | +76.9% | 44.5% | -15.4% | 1.73 | +73.6% | 2.19 |
| riesgoso_cedears | actual, sin filtros | +83.0% | 45.9% | -17.6% | 1.81 | +73.6% | 2.19 |
| riesgoso_acciones_arg | actual (12m) | +34.8% | 63.5% | -58.0% | 0.55 | +88.0% | 1.4 |
| riesgoso_acciones_arg | v0.1 (3m+6m / vol, RSI) | +18.6% | 51.7% | -64.6% | 0.36 | +88.0% | 1.4 |
| riesgoso_acciones_arg | 6m+12m / vol | +39.4% | 53.6% | -56.7% | 0.73 | +88.0% | 1.4 |
| riesgoso_acciones_arg | actual, top 5 | +46.6% | 57.0% | -59.9% | 0.82 | +88.0% | 1.4 |
| riesgoso_acciones_arg | actual, sin filtros | +37.1% | 58.0% | -58.9% | 0.64 | +88.0% | 1.4 |

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
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- bcra_badlar_serie: ok

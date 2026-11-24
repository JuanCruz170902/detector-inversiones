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

- AL30: TIR 20.55% · duration 1.63 · precio USD 47.564
- AL29: TIR 19.56% · duration 1.24 · precio USD 48.37
- GD30: TIR 17.86% · duration 1.65 · precio USD 49.358
- GD29: TIR 15.75% · duration 1.26 · precio USD 50.37

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.41% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57136 VN | $ 79.790 | $ 209 |
| dollar_linked | D31M7 | 37 VN | $ 58.312 | $ 152 |
| cer | TZXM7 | 16755 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.538 | $ 0 |

Paper trading: valor $ 199.631 sobre $ 200.000 aportados (-0.18%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.41% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42852 VN | $ 59.843 | $ 156 |
| cedears_etf | XLF | 1 acciones | $ 50.250 | $ 314 |
| hard_dollar | AL30 | 49 VN | $ 39.391 | $ 103 |
| cer | TZXM7 | 8377 VN | $ 19.946 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 29.945 | $ 0 |

Paper trading: valor $ 199.581 sobre $ 200.000 aportados (-0.21%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.19% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.41% mensual vs 2.77% del último mes → cobertura barata.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| acciones_arg | TXAR | 70 acciones | $ 49.350 | $ 308 |
| cedears | MSFT | 1 acciones | $ 29.680 | $ 185 |
| cedears | CVX | 1 acciones | $ 23.460 | $ 147 |
| cedears | WMT | 2 acciones | $ 26.180 | $ 163 |
| tasa_fija | T30A7 | 21426 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 40.527 | $ 0 |

Paper trading: valor $ 198.841 sobre $ 200.000 aportados (-0.58%); mismos aportes en MEP: $ 200.000.

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +12.1% | +5.2% (SPY) | -16.1% |
| riesgoso_cedears | 2013-05-31 a 2026-11-30 | +54.3% | +nan% (SPY) | -29.1% |
| riesgoso_acciones_arg | 2001-08-31 a 2026-11-30 | +24.2% | +48.5% (igual peso del universo) | -79.2% |

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
- data912_historia: fallaron 4: GLD, PG, NU, VIST

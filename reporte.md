# Detector de oportunidades — 2026-11-26

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.56
- Dólar oficial: 1630.0
- Dólar MEP: 1688.7
- Dólar CCL: 1767.9
- Riesgo país (pb): 1067.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 4.42

## Curva en pesos: inflación implícita

| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |
|---|---|---|---|---|
| T15E7 | 28.69% | X29E7 | 1.44% | 2.0% |
| S29E7 | 28.71% | X29E7 | 1.44% | 2.0% |
| S26F7 | 30.6% | X29E7 | 1.44% | 2.13% |
| T30A7 | 33.44% | TZXA7 | 4.35% | 2.07% |
| T31Y7 | 33.73% | TZX27 | 4.42% | 2.08% |
| T30J7 | 34.04% | TZX27 | 4.42% | 2.1% |

## Soberanos en dólares

- AL30: TIR 18.45% · duration 1.64 · paridad 76.6% · precio USD 49.0
- GD30: TIR 16.84% · duration 1.66 · paridad 78.3% · precio USD 50.12
- AL29: TIR 16.04% · duration 1.25 · paridad 83.8% · precio USD 50.25
- GD29: TIR 15.26% · duration 1.26 · paridad 84.5% · precio USD 50.68
- AE38: TIR 17.16% · duration 3.88 · paridad 63.3% · precio USD 63.3
- AL41: TIR 15.62% · duration 5.04 · paridad 56.4% · precio USD 56.39
- AL35: TIR 15.36% · duration 5.0 · paridad 61.8% · precio USD 61.8
- GD38: TIR 14.25% · duration 4.1 · paridad 70.0% · precio USD 69.98
- GD35: TIR 13.89% · duration 5.07 · paridad 65.9% · precio USD 65.93
- GD41: TIR 13.57% · duration 5.27 · paridad 61.8% · precio USD 61.82
- GD46: TIR 13.08% · duration 5.49 · paridad 62.9% · precio USD 57.16

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.86% mensual vs 4.42% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57321 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.763 | $ 154 |
| cer | TZXM7 | 16808 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.085 | $ 0 |

Paper trading: valor $ 199.844 sobre $ 200.000 aportados (-0.08%); mismos aportes en MEP: $ 193.758.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.86% mensual vs 4.42% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42991 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 48 VN | $ 39.264 | $ 103 |
| cedears_etf | SPY | 1 acciones | $ 21.450 | $ 134 |
| cedears_etf | EEM | 1 acciones | $ 19.980 | $ 125 |
| cer | TZXM7 | 8404 VN | $ 19.947 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 38.946 | $ 0 |

Paper trading: valor $ 200.365 sobre $ 200.000 aportados (+0.18%); mismos aportes en MEP: $ 193.758.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.86% mensual vs 4.42% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.260 | $ 176 |
| cedears | WMT | 2 acciones | $ 26.080 | $ 163 |
| cedears | PBR | 1 acciones | $ 28.600 | $ 179 |
| tasa_fija | T30A7 | 21495 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 23.738 | $ 148 |
| acciones_arg | PAMP | 5 acciones | $ 22.200 | $ 139 |
| liquidez | CAUCION/FCI MM |  | $ 40.318 | $ 0 |

Paper trading: valor $ 198.044 sobre $ 200.000 aportados (-0.98%); mismos aportes en MEP: $ 193.758.

## Empresas en las propuestas

| Empresa | Datos hasta | Margen neto | ROE | P/E | Alertas |
|---|---|---|---|---|---|
| GGAL (Grupo Financiero Galicia Sa) | 2025-03-31 6-K | – | 23% | – | último dato en la SEC: 2025-03-31 |
| PAMP (Pampa Energy Inc.) | 2024-12-31 20-F | 33.0% | 19% | – | último dato en la SEC: 2024-12-31 |
| PBR (Petrobras - Petroleo Brasileiro Sa) | 2025-06-30 6-K/A | 16.0% | 19% | – | ventas -14% interanual; último dato en la SEC: 2025-06-30 |
| WMT (Walmart Inc.) | 2026-07-31 10-Q | 3.0% | 22% | 47.9 | – |
| XOM (Exxonmobil Holdings Corp) | 2026-09-30 10-Q | 10.2% | 15% | 16.3 | – |
- GGAL: Grupo Financiero Galicia Q3 2026 Earnings Call Is Live - TradingView (TradingView, 2026-11-25)
- GGAL: Informe de resultados: Grupo Financiero Galicia SA ADR no alcanza el BPA del tercer trimestre de 2026 - Investing.com España (Investing.com España, 2026-11-25)
- GGAL: Grupo Financiero Galicia vuelve al verde: ¿Cuánto bajó la mora en el tercer trimestre? - Bloomberg Línea (Bloomberg Línea, 2026-11-24)
- PAMP: La central de Timbúes entra en la estrategia de expansión eléctrica de Pampa Energía - IRE Somos Región (IRE Somos Región, 2026-11-23)
- PBR: Petrobras Eyes Corn Ethanol Expansion: Can It Unlock New Value? (Yahoo Finance, 2026-11-25)
- PBR: Petrobras Unveils $122 Billion Plan, Sees Potential for $10 Billion More in Dividends (Yahoo Finance, 2026-11-25)
- PBR: Can Brazil's Fuel Crackdown Help UGP's Ipiranga Gain More Share? (Yahoo Finance, 2026-11-24)
- WMT: Jensen Huang's return, neocloud risk, and a holiday retail rally (Yahoo Finance, 2026-11-25)
- WMT: Tariffs are back as Anthropic sinks further below its IPO price (Yahoo Finance, 2026-11-25)
- WMT: Ten reasons the market is selling off again before Thanksgiving (Yahoo Finance, 2026-11-25)
- XOM: ExxonMobil (XOM) Stock Looks Cheap Against Future Cash Flow Estimates (Yahoo Finance, 2026-11-25)
- XOM: Bad News for Exxon and Chevron: Goldman Sees Brent Falling “Roughly $10” Next Year on a Supply Glut (Yahoo Finance, 2026-11-25)
- XOM: Turn $100,000 Into Lifetime Paychecks With These “Forever” Passive Income Dividend Stocks (Yahoo Finance, 2026-11-25)

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +43.8% | +48.9% (SPY) | -17.6% |
| riesgoso_cedears | 2023-02-28 a 2026-11-30 | +81.3% | +75.2% (SPY) | -17.6% |
| riesgoso_acciones_arg | 2022-12-31 a 2026-11-30 | +34.8% | +89.2% (igual peso del universo) | -58.1% |

### Variantes de la regla

| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |
|---|---|---|---|---|---|---|---|
| moderado_cedears_etf | actual (12m) | +43.8% | 22.9% | -17.6% | 1.91 | +48.9% | 1.68 |
| moderado_cedears_etf | v0.1 (3m+6m / vol, RSI) | +32.5% | 21.9% | -27.4% | 1.49 | +48.9% | 1.68 |
| moderado_cedears_etf | 6m+12m / vol | +40.8% | 22.1% | -18.9% | 1.84 | +48.9% | 1.68 |
| moderado_cedears_etf | actual, top 5 | +59.2% | 20.1% | -13.6% | 2.95 | +75.2% | 2.24 |
| moderado_cedears_etf | actual, sin filtros | +43.3% | 24.5% | -16.3% | 1.77 | +48.9% | 1.68 |
| riesgoso_cedears | actual (12m) | +81.3% | 45.7% | -17.6% | 1.78 | +75.2% | 2.24 |
| riesgoso_cedears | v0.1 (3m+6m / vol, RSI) | +41.5% | 39.6% | -25.8% | 1.05 | +75.2% | 2.24 |
| riesgoso_cedears | 6m+12m / vol | +63.9% | 34.2% | -15.8% | 1.86 | +75.2% | 2.24 |
| riesgoso_cedears | actual, top 5 | +76.4% | 44.6% | -15.4% | 1.71 | +75.2% | 2.24 |
| riesgoso_cedears | actual, sin filtros | +82.1% | 46.1% | -17.6% | 1.78 | +75.2% | 2.24 |
| riesgoso_acciones_arg | actual (12m) | +34.8% | 63.5% | -58.1% | 0.55 | +89.2% | 1.42 |
| riesgoso_acciones_arg | v0.1 (3m+6m / vol, RSI) | +18.1% | 51.8% | -65.1% | 0.35 | +89.2% | 1.42 |
| riesgoso_acciones_arg | 6m+12m / vol | +39.3% | 53.6% | -56.8% | 0.73 | +89.2% | 1.42 |
| riesgoso_acciones_arg | actual, top 5 | +47.3% | 56.8% | -59.1% | 0.83 | +89.2% | 1.42 |
| riesgoso_acciones_arg | actual, sin filtros | +37.0% | 58.0% | -59.0% | 0.64 | +89.2% | 1.42 |

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
- calendario_balances: ok (nasdaq, 141 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- data912_usa: ok
- sec_y_noticias: ok (30 balances, 29 con noticias)
- bcra_badlar_serie: ok

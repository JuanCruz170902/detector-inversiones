# Detector de oportunidades — 2026-11-27

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.56
- Dólar oficial: 1630.0
- Dólar MEP: 1688.7
- Dólar CCL: 1767.9
- Riesgo país (pb): 1067.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 4.03

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

- AL30: TIR 17.9% · duration 1.65 · paridad 77.2% · precio USD 49.4
- GD30: TIR 15.65% · duration 1.67 · paridad 79.7% · precio USD 51.0
- AL29: TIR 13.28% · duration 1.27 · paridad 86.4% · precio USD 51.82
- GD29: TIR 12.34% · duration 1.28 · paridad 87.3% · precio USD 52.37
- AE38: TIR 16.2% · duration 3.95 · paridad 65.4% · precio USD 65.4
- AL35: TIR 15.0% · duration 5.02 · paridad 62.8% · precio USD 62.8
- AL41: TIR 14.82% · duration 5.13 · paridad 58.4% · precio USD 58.43
- GD38: TIR 13.78% · duration 4.13 · paridad 71.2% · precio USD 71.21
- GD35: TIR 13.66% · duration 5.07 · paridad 66.6% · precio USD 66.63
- GD41: TIR 13.16% · duration 5.32 · paridad 63.0% · precio USD 63.05
- GD46: TIR 12.8% · duration 5.54 · paridad 63.7% · precio USD 57.95

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.00% mensual vs 4.03% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57321 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.682 | $ 153 |
| cer | TZXM7 | 16808 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.167 | $ 0 |

Paper trading: valor $ 200.671 sobre $ 200.000 aportados (+0.34%); mismos aportes en MEP: $ 193.758.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.00% mensual vs 4.03% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42991 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 48 VN | $ 39.432 | $ 103 |
| cedears_etf | SPY | 1 acciones | $ 21.600 | $ 135 |
| cedears_etf | EEM | 1 acciones | $ 20.270 | $ 127 |
| cer | TZXM7 | 8404 VN | $ 19.947 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 38.334 | $ 0 |

Paper trading: valor $ 202.920 sobre $ 200.000 aportados (+1.46%); mismos aportes en MEP: $ 193.758.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.06% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.00% mensual vs 4.03% del último mes → cobertura barata.
- Brecha MEP/oficial 3.6%.
- Riesgo país 1067 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.780 | $ 180 |
| cedears | WMT | 2 acciones | $ 25.840 | $ 161 |
| cedears | PBR | 1 acciones | $ 29.500 | $ 184 |
| tasa_fija | T30A7 | 21495 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 24.450 | $ 153 |
| acciones_arg | BMA | 2 acciones | $ 18.320 | $ 114 |
| liquidez | CAUCION/FCI MM |  | $ 42.318 | $ 0 |

Paper trading: valor $ 198.185 sobre $ 200.000 aportados (-0.91%); mismos aportes en MEP: $ 193.758.

## Empresas en las propuestas

| Empresa | Datos hasta | Margen neto | ROE | P/E | Alertas |
|---|---|---|---|---|---|
| BMA (Macro Bank Inc.) | 2024-12-31 20-F | – | 8% | – | último dato en la SEC: 2024-12-31 |
| GGAL (Grupo Financiero Galicia Sa) | 2025-03-31 6-K | – | 23% | – | último dato en la SEC: 2025-03-31 |
| PBR (Petrobras - Petroleo Brasileiro Sa) | 2025-06-30 6-K/A | 16.0% | 19% | – | ventas -14% interanual; último dato en la SEC: 2025-06-30 |
| WMT (Walmart Inc.) | 2026-07-31 10-Q | 3.0% | 22% | 47.8 | – |
| XOM (Exxonmobil Holdings Corp) | 2026-09-30 10-Q | 10.2% | 15% | 16.3 | – |
- BMA: Banco Macro revierte su pérdida neta del 2025 pero sube la mora y ceden sus préstamos - Bloomberg Línea (Bloomberg Línea, 2026-11-26)
- BMA: Banco Macro S.A.: precio objetivo a 12 meses baja a $106.43; potencial subida del 111% - TradingView (TradingView, 2026-11-26)
- BMA: Banco Macro B ADR no alcanza por 0,16$ las previsiones de BPA en el tercer trimestre del año - Investing.com España (Investing.com España, 2026-11-26)
- GGAL: Grupo Financiero Galicia vuelve al verde: ¿Cuánto bajó la mora en el tercer trimestre? - Bloomberg Línea (Bloomberg Línea, 2026-11-24)
- GGAL: Grupo Galicia volvió a obtener ganancias y redujo la presión de la morosidad en su último balance - Forbes Argentina (Forbes Argentina, 2026-11-24)
- GGAL: Grupo Galicia gana ARS$229.002M y baja la mora a 9,7% - El Ecosistema Startup (El Ecosistema Startup, 2026-11-24)
- PBR: Ultrapar Outperforms Petrobras YTD: Why PBR Still Has the Edge (Yahoo Finance, 2026-11-26)
- PBR: Petrobras Eyes Corn Ethanol Expansion: Can It Unlock New Value? (Yahoo Finance, 2026-11-25)
- PBR: Petrobras Unveils $122 Billion Plan, Sees Potential for $10 Billion More in Dividends (Yahoo Finance, 2026-11-25)
- WMT: 3 big reasons why Black Friday will probably exceed retailer expectations (Yahoo Finance, 2026-11-26)
- WMT: Forget Walmart: Nike Has More to Lose From Vietnam’s Proposed Tariff of Up to 35% (Yahoo Finance, 2026-11-27)
- WMT: Walmart (WMT) Stock Gets Fair Value Boost After Q3 Price Target Increases (Yahoo Finance, 2026-11-27)
- XOM: ExxonMobil (XOM) Stock Looks Cheap Against Future Cash Flow Estimates (Yahoo Finance, 2026-11-25)
- XOM: Bad News for Exxon and Chevron: Goldman Sees Brent Falling “Roughly $10” Next Year on a Supply Glut (Yahoo Finance, 2026-11-25)
- XOM: Turn $100,000 Into Lifetime Paychecks With These “Forever” Passive Income Dividend Stocks (Yahoo Finance, 2026-11-25)

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +44.4% | +49.2% (SPY) | -17.6% |
| riesgoso_cedears | 2023-02-28 a 2026-11-30 | +82.3% | +75.5% (SPY) | -17.6% |
| riesgoso_acciones_arg | 2022-12-31 a 2026-11-30 | +35.7% | +90.4% (igual peso del universo) | -56.9% |

### Variantes de la regla

| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |
|---|---|---|---|---|---|---|---|
| moderado_cedears_etf | actual (12m) | +44.4% | 22.8% | -17.6% | 1.95 | +49.2% | 1.69 |
| moderado_cedears_etf | v0.1 (3m+6m / vol, RSI) | +32.6% | 21.9% | -27.4% | 1.49 | +49.2% | 1.69 |
| moderado_cedears_etf | 6m+12m / vol | +40.9% | 22.1% | -18.9% | 1.85 | +49.2% | 1.69 |
| moderado_cedears_etf | actual, top 5 | +59.6% | 20.1% | -13.6% | 2.97 | +75.5% | 2.25 |
| moderado_cedears_etf | actual, sin filtros | +43.9% | 24.4% | -16.3% | 1.8 | +49.2% | 1.69 |
| riesgoso_cedears | actual (12m) | +82.3% | 45.5% | -17.6% | 1.81 | +75.5% | 2.25 |
| riesgoso_cedears | v0.1 (3m+6m / vol, RSI) | +41.4% | 39.6% | -25.8% | 1.05 | +75.5% | 2.25 |
| riesgoso_cedears | 6m+12m / vol | +63.8% | 34.2% | -15.8% | 1.86 | +75.5% | 2.25 |
| riesgoso_cedears | actual, top 5 | +76.9% | 44.5% | -15.4% | 1.73 | +75.5% | 2.25 |
| riesgoso_cedears | actual, sin filtros | +83.0% | 45.9% | -17.6% | 1.81 | +75.5% | 2.25 |
| riesgoso_acciones_arg | actual (12m) | +35.7% | 63.3% | -56.9% | 0.56 | +90.4% | 1.44 |
| riesgoso_acciones_arg | v0.1 (3m+6m / vol, RSI) | +18.9% | 51.6% | -64.3% | 0.37 | +90.4% | 1.44 |
| riesgoso_acciones_arg | 6m+12m / vol | +40.6% | 53.3% | -55.2% | 0.76 | +90.4% | 1.44 |
| riesgoso_acciones_arg | actual, top 5 | +48.2% | 56.7% | -58.1% | 0.85 | +90.4% | 1.44 |
| riesgoso_acciones_arg | actual, sin filtros | +38.0% | 57.8% | -57.8% | 0.66 | +90.4% | 1.44 |

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
- calendario_balances: ok (nasdaq, 147 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- data912_usa: ok
- sec_y_noticias: ok (30 balances, 28 con noticias)
- bcra_badlar_serie: ok

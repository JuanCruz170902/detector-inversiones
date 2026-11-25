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

- AL30: TIR 19.9% · duration 1.63 · paridad 75.0% · precio USD 48.009
- AL29: TIR 17.83% · duration 1.25 · paridad 82.1% · precio USD 49.276
- GD30: TIR 17.38% · duration 1.66 · paridad 77.7% · precio USD 49.716
- GD29: TIR 16.15% · duration 1.26 · paridad 83.6% · precio USD 50.17
- AE38: TIR 17.17% · duration 3.88 · paridad 63.2% · precio USD 63.25
- AL35: TIR 15.77% · duration 4.99 · paridad 60.7% · precio USD 60.7
- AL41: TIR 15.55% · duration 5.05 · paridad 56.5% · precio USD 56.52
- GD38: TIR 14.63% · duration 4.07 · paridad 69.0% · precio USD 69.02
- GD35: TIR 14.37% · duration 5.05 · paridad 64.5% · precio USD 64.51
- GD41: TIR 13.87% · duration 5.24 · paridad 60.9% · precio USD 60.94
- GD46: TIR 13.22% · duration 5.47 · paridad 62.4% · precio USD 56.74

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.19% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 57350 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.697 | $ 153 |
| cer | TZXA7 | 30489 VN | $ 39.895 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.151 | $ 0 |

Paper trading: valor $ 200.117 sobre $ 200.000 aportados (+0.06%); mismos aportes en MEP: $ 194.493.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.19% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 43012 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 49 VN | $ 39.107 | $ 102 |
| cedears_etf | SPY | 1 acciones | $ 20.920 | $ 131 |
| cedears_etf | EEM | 1 acciones | $ 19.640 | $ 123 |
| cer | TZXA7 | 15244 VN | $ 19.947 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 39.980 | $ 0 |

Paper trading: valor $ 199.636 sobre $ 200.000 aportados (-0.18%); mismos aportes en MEP: $ 194.493.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.17% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 2.19% mensual vs 3.46% del último mes → cobertura barata.
- Brecha MEP/oficial 5.0%.
- Riesgo país 1094 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | XOM | 1 acciones | $ 28.020 | $ 175 |
| cedears | WMT | 2 acciones | $ 25.740 | $ 161 |
| cedears | PBR | 1 acciones | $ 28.300 | $ 177 |
| tasa_fija | T30A7 | 21506 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 22.850 | $ 143 |
| acciones_arg | PAMP | 6 acciones | $ 26.070 | $ 163 |
| liquidez | CAUCION/FCI MM |  | $ 38.202 | $ 0 |

Paper trading: valor $ 194.929 sobre $ 200.000 aportados (-2.54%); mismos aportes en MEP: $ 194.493.

## Empresas en las propuestas

| Empresa | Último balance | Margen neto | ROE | P/E | Alertas |
|---|---|---|---|---|---|
| GGAL (Grupo Financiero Galicia Sa) | 2025-06-10 6-K | – | 23% | – | sin balances recientes en la SEC |
| PAMP (Pampa Energy Inc.) | 2025-04-16 20-F | 33.0% | 19% | – | sin balances recientes en la SEC |
| PBR (Petrobras - Petroleo Brasileiro Sa) | 2025-08-26 6-K/A | 16.0% | 19% | – | ventas -14% interanual; sin balances recientes en la SEC |
| WMT (Walmart Inc.) | 2026-08-28 10-Q | 3.0% | 22% | 47.8 | – |
| XOM (Exxonmobil Holdings Corp) | 2026-11-02 10-Q | – | – | – | – |
- GGAL: Grupo Financiero Galicia vuelve al verde: ¿Cuánto bajó la mora en el tercer trimestre? - Bloomberg Línea (Bloomberg Línea, 2026-11-24)
- GGAL: Grupo Financiero Galicia S.A.: precio objetivo a 12 meses baja a $61.47; potencial subida del 131% - TradingView (TradingView, 2026-11-24)
- GGAL: Grupo Galicia volvió a obtener ganancias y redujo la presión de la morosidad en su último balance - Forbes Argentina (Forbes Argentina, 2026-11-24)
- PAMP: Gráfico interactivo de acciones de Pampa Energia SA (9PAA.HA) - Yahoo Finanzas (Yahoo Finanzas, 2026-11-23)
- PAMP: Pampa Energía busca ampliar su participación en tres centrales eléctricas que el Gobierno privatizará - Diario Neuquino (Diario Neuquino, 2026-11-22)
- PBR: Petrobras Unveils $122 Billion Plan, Sees Potential for $10 Billion More in Dividends (Yahoo Finance, 2026-11-25)
- PBR: Can Brazil's Fuel Crackdown Help UGP's Ipiranga Gain More Share? (Yahoo Finance, 2026-11-24)
- PBR: Petrobras Unveils $122B Investment Plan, Eyes Higher Dividends (Yahoo Finance, 2026-11-24)
- WMT: Ten reasons the market is selling off again before Thanksgiving (Yahoo Finance, 2026-11-25)
- WMT: Tanking gas prices could be the setup needed for strong holiday season (Yahoo Finance, 2026-11-25)
- WMT: Amazon and Meta are negotiating the future of AI shopping. Consumers aren't quite there yet. (Yahoo Finance, 2026-11-25)
- XOM: Bad News for Exxon and Chevron: Goldman Sees Brent Falling “Roughly $10” Next Year on a Supply Glut (Yahoo Finance, 2026-11-25)
- XOM: Turn $100,000 Into Lifetime Paychecks With These “Forever” Passive Income Dividend Stocks (Yahoo Finance, 2026-11-25)
- XOM: Global Ethyl Derivatives Market Report 2026: Executive Strategy and Forecast to 2030 | Capitalize on Bio-Based and Pharma Demand with BASF, Dow, Arkema, Clariant, and Exxon Mobil (Yahoo Finance, 2026-11-25)

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
- calendario_balances: ok (nasdaq, 170 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- data912_usa: ok
- sec_y_noticias: ok (30 balances, 29 con noticias)
- bcra_badlar_serie: ok

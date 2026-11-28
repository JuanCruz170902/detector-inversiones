# Detector de oportunidades — 2026-11-28

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.62
- Dólar oficial: 1625.0
- Dólar MEP: 1661.9
- Dólar CCL: 1751.3
- Riesgo país (pb): 960.0
- Inflación esperada mensual (%): 1.66
- Devaluación A3500 último mes (%): 4.06

## Curva en pesos: inflación implícita

| Tasa fija | TEA | CER | TIR real | Inflación implícita mensual |
|---|---|---|---|---|
| T15E7 | 26.65% | X29E7 | -0.42% | 2.02% |
| S29E7 | 27.81% | X29E7 | -0.42% | 2.1% |
| S26F7 | 28.61% | X29E7 | -0.42% | 2.15% |
| T30A7 | 32.0% | TZXA7 | 2.58% | 2.12% |
| T31Y7 | 32.53% | TZXY7 | 3.8% | 2.06% |
| T30J7 | 33.2% | TZX27 | 4.09% | 2.08% |
| TY30P | 31.85% | TXMJ0 | 7.72% | 1.7% |

## Soberanos en dólares

- AL30: TIR 17.63% · duration 1.65 · paridad 77.5% · precio USD 49.61
- AL29: TIR 15.2% · duration 1.25 · paridad 84.6% · precio USD 50.75
- GD30: TIR 14.89% · duration 1.68 · paridad 80.6% · precio USD 51.59
- GD29: TIR 13.61% · duration 1.26 · paridad 86.1% · precio USD 51.65
- AE38: TIR 15.51% · duration 4.0 · paridad 67.0% · precio USD 67.0
- AL35: TIR 14.56% · duration 5.03 · paridad 64.0% · precio USD 64.04
- AL41: TIR 14.36% · duration 5.18 · paridad 59.7% · precio USD 59.67
- GD35: TIR 13.31% · duration 5.09 · paridad 67.7% · precio USD 67.7
- GD38: TIR 13.01% · duration 4.19 · paridad 73.3% · precio USD 73.26
- GD41: TIR 12.93% · duration 5.34 · paridad 63.8% · precio USD 63.76
- GD46: TIR 12.2% · duration 5.66 · paridad 65.7% · precio USD 59.72

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Inflación implícita 2.09% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.91% mensual vs 4.06% del último mes → cobertura barata.
- Brecha MEP/oficial 2.3%.
- Riesgo país 960 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 56884 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 37 VN | $ 58.749 | $ 154 |
| cer | TZXM7 | 16699 VN | $ 39.894 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 21.100 | $ 0 |

Paper trading: valor $ 200.890 sobre $ 200.000 aportados (+0.44%); mismos aportes en MEP: $ 190.683.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Inflación implícita 2.09% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.91% mensual vs 4.06% del último mes → cobertura barata.
- Brecha MEP/oficial 2.3%.
- Riesgo país 960 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T30A7 | 42663 VN | $ 59.843 | $ 156 |
| hard_dollar | AL30 | 48 VN | $ 39.456 | $ 103 |
| cedears_etf | SPY | 1 acciones | $ 21.420 | $ 134 |
| cedears_etf | EEM | 1 acciones | $ 20.540 | $ 128 |
| cer | TZXM7 | 8349 VN | $ 19.946 | $ 52 |
| liquidez | CAUCION/FCI MM |  | $ 38.221 | $ 0 |

Paper trading: valor $ 201.505 sobre $ 200.000 aportados (+0.75%); mismos aportes en MEP: $ 190.683.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Inflación implícita 2.09% mensual vs esperada 1.66%: el mercado descuenta MÁS inflación de la esperada → conviene tasa fija.
- Dollar linked: devaluación implícita 1.91% mensual vs 4.06% del último mes → cobertura barata.
- Brecha MEP/oficial 2.3%.
- Riesgo país 960 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears | CVX | 1 acciones | $ 23.420 | $ 146 |
| cedears | XOM | 1 acciones | $ 28.400 | $ 177 |
| cedears | WMT | 2 acciones | $ 25.940 | $ 162 |
| tasa_fija | T30A7 | 21331 VN | $ 29.921 | $ 78 |
| acciones_arg | GGAL | 5 acciones | $ 24.900 | $ 156 |
| acciones_arg | BMA | 2 acciones | $ 18.440 | $ 115 |
| liquidez | CAUCION/FCI MM |  | $ 48.144 | $ 0 |

Paper trading: valor $ 198.303 sobre $ 200.000 aportados (-0.85%); mismos aportes en MEP: $ 190.683.

## Empresas en las propuestas

| Empresa | Datos hasta | Margen neto | ROE | P/E | Alertas |
|---|---|---|---|---|---|
| BMA (Macro Bank Inc.) | 2024-12-31 20-F | – | 8% | – | último dato en la SEC: 2024-12-31 |
| CVX (Chevron Corp) | 2026-09-30 10-Q | 11.6% | 14% | 15.7 | – |
| GGAL (Grupo Financiero Galicia Sa) | 2025-03-31 6-K | – | 23% | – | último dato en la SEC: 2025-03-31 |
| WMT (Walmart Inc.) | 2026-07-31 10-Q | 3.0% | 22% | 48.3 | – |
| XOM (Exxonmobil Holdings Corp) | 2026-09-30 10-Q | 10.2% | 15% | 16.6 | – |
- BMA: Banco Macro S.A. (BMA) anuncia los resultados del tercer trimestre de 2026 - TradingView (TradingView, 2026-11-25)
- BMA: Banco Macro revierte su pérdida neta del 2025 pero sube la mora y ceden sus préstamos - Bloomberg Línea (Bloomberg Línea, 2026-11-26)
- BMA: Banco Macro S A : anuncia Resultados del tercer trimestre del 2026 - MarketScreener España (MarketScreener España, 2026-11-25)
- CVX: What's Going On With Chevron Stock On Friday? (Yahoo Finance, 2026-11-27)
- CVX: Chevron Corporation (CVX) Is a Trending Stock: Facts to Know Before Betting on It (Yahoo Finance, 2026-11-27)
- CVX: Chevron Stock Leads The Oil Price Shock Theme For Integrated Energy Investors (Yahoo Finance, 2026-11-27)
- GGAL: Grupo Financiero Galicia vuelve al verde: ¿Cuánto bajó la mora en el tercer trimestre? - Bloomberg Línea (Bloomberg Línea, 2026-11-24)
- GGAL: Grupo Financiero Galicia S.A.: precio objetivo a 12 meses baja a $61.47; potencial subida del 131% - TradingView (TradingView, 2026-11-24)
- GGAL: Informe de resultados: Grupo Financiero Galicia SA ADR no alcanza el BPA del tercer trimestre de 2026 - Investing.com España (Investing.com España, 2026-11-25)
- WMT: How AI is driving record holiday spending (Yahoo Finance, 2026-11-27)
- WMT: Learn Why The Bull Case For Walmart (WMT) Could Change Following Earnings Beat (Yahoo Finance, 2026-11-28)
- WMT: Walmart bets shoppers won't notice its holiday price increases (Yahoo Finance, 2026-11-28)
- XOM: How Is ExxonMobil’s Stock Performance Compared to Other Oil & Gas Stocks (Yahoo Finance, 2026-11-27)
- XOM: XOM Boosts Angola Prospects With Kizomba Redevelopment & New Discovery (Yahoo Finance, 2026-11-27)
- XOM: ExxonMobil Holdings Corporation (XOM) is Attracting Investor Attention: Here is What You Should Know (Yahoo Finance, 2026-11-27)

## Backtest de la regla de renta variable

| Caso | Período | Estrategia (anual) | Benchmark (anual) | Máx. caída estrategia |
|---|---|---|---|---|
| moderado_cedears_etf | 2023-09-30 a 2026-11-30 | +44.7% | +48.8% (SPY) | -17.6% |
| riesgoso_cedears | 2023-02-28 a 2026-11-30 | +82.5% | +75.1% (SPY) | -17.6% |
| riesgoso_acciones_arg | 2022-12-31 a 2026-11-30 | +35.4% | +90.5% (igual peso del universo) | -57.3% |

### Variantes de la regla

| Caso | Variante | Anual | Vol | Máx. caída | Anual/Vol | Benchmark anual | Bench Anual/Vol |
|---|---|---|---|---|---|---|---|
| moderado_cedears_etf | actual (12m) | +44.7% | 22.8% | -17.6% | 1.96 | +48.8% | 1.67 |
| moderado_cedears_etf | v0.1 (3m+6m / vol, RSI) | +32.5% | 21.9% | -27.4% | 1.48 | +48.8% | 1.67 |
| moderado_cedears_etf | 6m+12m / vol | +40.7% | 22.1% | -18.9% | 1.84 | +48.8% | 1.67 |
| moderado_cedears_etf | actual, top 5 | +59.7% | 20.0% | -13.6% | 2.98 | +75.1% | 2.24 |
| moderado_cedears_etf | actual, sin filtros | +44.2% | 24.4% | -16.3% | 1.81 | +48.8% | 1.67 |
| riesgoso_cedears | actual (12m) | +82.5% | 45.4% | -17.6% | 1.82 | +75.1% | 2.24 |
| riesgoso_cedears | v0.1 (3m+6m / vol, RSI) | +41.2% | 39.6% | -25.8% | 1.04 | +75.1% | 2.24 |
| riesgoso_cedears | 6m+12m / vol | +63.5% | 34.2% | -15.8% | 1.85 | +75.1% | 2.24 |
| riesgoso_cedears | actual, top 5 | +76.9% | 44.5% | -15.4% | 1.73 | +75.1% | 2.24 |
| riesgoso_cedears | actual, sin filtros | +83.3% | 45.9% | -17.6% | 1.82 | +75.1% | 2.24 |
| riesgoso_acciones_arg | actual (12m) | +35.4% | 63.4% | -57.3% | 0.56 | +90.5% | 1.44 |
| riesgoso_acciones_arg | v0.1 (3m+6m / vol, RSI) | +18.7% | 51.6% | -64.5% | 0.36 | +90.5% | 1.44 |
| riesgoso_acciones_arg | 6m+12m / vol | +40.1% | 53.4% | -55.8% | 0.75 | +90.5% | 1.44 |
| riesgoso_acciones_arg | actual, top 5 | +47.9% | 56.7% | -58.5% | 0.84 | +90.5% | 1.44 |
| riesgoso_acciones_arg | actual, sin filtros | +37.6% | 57.8% | -58.3% | 0.65 | +90.5% | 1.44 |

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
- calendario_balances: ok (nasdaq, 187 empresas)
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok
- data912_usa: ok
- sec_y_noticias: ok (30 balances, 28 con noticias)
- bcra_badlar_serie: ok

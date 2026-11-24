# Reglas del detector (v0.2, demo)

Todas las reglas viven en [`config/perfiles.yaml`](config/perfiles.yaml). Este documento explica qué hace cada una y por qué.

> Herramienta personal de análisis. No es asesoramiento financiero: la decisión y la ejecución de cada orden son del usuario.

## 1. Universo

| Bucket | Qué es | Cómo se detecta | Cómo se elige |
|---|---|---|---|
| `cer` | Bonos y letras ajustados por inflación | ArgentinaDatos `/finanzas/bonos-cer` (TIR real) | líquido → dentro del horizonte → **más barato contra la curva** → mayor TIR real |
| `tasa_fija` | LECAP y BONCAP | ArgentinaDatos `/finanzas/letras` (TEA/TEM) | líquido → dentro del horizonte → más barato contra la curva → mayor TEA |
| `dollar_linked` | Letras atadas al A3500 (D…) | panel data912 + A3500 del BCRA | líquido → dentro del horizonte → **menor devaluación breakeven** |
| `hard_dollar` | Soberanos en USD (AL/GD), especie en pesos | lista en `universo.yaml` | líquido → **mayor TIR en USD** (flujos AL29/GD29/AL30/GD30) |
| `cedears_etf` | CEDEARs de ETFs amplios | lista en `universo.yaml` | score de momentum ajustado por riesgo |
| `cedears` | CEDEARs individuales + ETFs | lista | ídem |
| `acciones_arg` | Panel líder Merval | lista | ídem |
| `liquidez` | Caución / FCI money market | — | remanente de cada reparto |

## 2. Reparto base por perfil (horizonte corto)

| Bucket | Conservador | Moderado | Riesgoso |
|---|---|---|---|
| CER | 35% | 20% | — |
| Tasa fija | 30% | 20% | 15% |
| Dollar linked | 20% | — | — |
| Hard dollar | — | 20% | — |
| CEDEARs ETF | — | 30% | — |
| CEDEARs | — | — | 45% |
| Acciones arg. | — | — | 40% |
| Liquidez | 15% | 10% | — |
| Máx. posiciones | 4 | 5 | 6 |
| Máx. por posición | 40% | 30% | 25% |

## 3. Ajustes automáticos con las curvas

Un bono solo se considera comprable si operó más de **$20 M** en el día. Con menos, el precio de pantalla no es ejecutable.

1. **Valor relativo.** Se ajusta una curva `rendimiento = a + b·ln(días)` con los papeles líquidos. El **residuo** (en puntos básicos) dice cuánto paga cada papel por encima o por debajo de sus vecinos, y se prefieren los de residuo positivo.
2. **CER vs tasa fija (breakeven de inflación).** Para cada LECAP/BONCAP se busca el CER de vencimiento más cercano:
   `inflación implícita = (1 + TEA fija) / (1 + TIR real CER) − 1`.
   El promedio en el horizonte se compara contra la **inflación esperada**: la mediana del REM del BCRA a 12 meses, mensualizada; si falta, el promedio de los últimos 3 meses.
   - Implícita > esperada + 0,15 pp → el mercado paga de más por la inflación → **tasa fija** (+10/15 pp desde CER).
   - Implícita < esperada − 0,15 pp → **CER**.
   - En el medio, neutral.
   - Si no hay curvas, se usa la regla anterior: plazo fijo mensual vs última inflación.
3. **Dollar linked (breakeven de devaluación).** Es el A3500 al vencimiento con el que el DL empata a la tasa fija del mismo plazo, en % mensual, comparado contra el ritmo del A3500 del último mes.
   - Breakeven < ritmo − 0,1 pp → cobertura **barata** (+10 pp desde liquidez).
   - Breakeven > ritmo + 0,5 pp → cobertura **cara** (−10 pp a tasa fija).
   - Brecha MEP/oficial > 15% también suma cobertura, salvo que esté cara.

## 4. Selección de renta variable

**CEDEARs (moderado y riesgoso): momentum de 12 meses.**
```
score = retorno de los últimos 12 meses
```

Filtros (descartan, no penalizan):
- **Todos:** score > 0 y volumen diario > $5 M.
- **Moderado:** además, precio arriba de la media de 200 ruedas y volatilidad < 35%.
- **Riesgoso:** además, volatilidad < 80%.

**Acciones argentinas: canasta por liquidez.** Las más operadas del panel líder con igual peso, sin intentar elegir ganadoras. Ver el porqué en §7.

> En la v0.1 la regla era `0,5·ret 3m + 0,5·ret 6m`, ajustada por volatilidad y penalizada con RSI > 75. El backtest mostró que rendía peor (§7).

## 5. Ejecución realista

- **Comisiones:** Cocos plan base, 0,45% en acciones/CEDEARs y 0,15% en bonos. Se suman IVA sobre la comisión y ~0,08% de derechos de mercado.
- **Cantidades enteras:** bonos y letras cotizan cada 100 VN. Lo que no alcanza para una unidad queda en liquidez.
- **Tamaño de posición:** ticket mínimo de $20.000. Posiciones más chicas, o que excedan el máximo de posiciones, van a liquidez.

## 6. Paper trading (fase de pruebas)

Cada perfil "invierte" $200.000 el primer día hábil de cada mes según la propuesta del día y se valúa a diario. La liquidez rinde la tasa de plazo fijo. Se compara contra:
- **Mismos aportes en dólar MEP:** ¿le ganamos al dólar?
- **Total aportado:** ¿le ganamos a no hacer nada?

## 7. Backtest de la regla de renta variable

Cada fin de mes, con la información disponible ese día, se eligen los mejores por score que pasan los filtros del perfil. Se mantienen un mes con igual peso y se descuenta comisión de compra y venta por la rotación.
- Ventana común de hasta 4 años.
- Benchmark: SPY para CEDEARs; igual peso del universo para acciones argentinas.
- Precios en pesos: los CEDEARs incluyen la variación del CCL.

Sirve para saber si la regla agrega valor contra comprar y mantener, no para prometer rendimientos.

**Resultado (corrida del 24/11/2026, en pesos, 2023–2026).** "Anual/Vol" es el rendimiento por unidad de riesgo: más alto es mejor.

| Caso | Regla v0.1 (3m+6m) | Momentum 12m | Comprar y mantener |
|---|---|---|---|
| Moderado, ETFs | +31,5% anual · Anual/Vol 1,43 | +43,3% · **1,96** | SPY +47,3% · 1,62 |
| Riesgoso, CEDEARs | +41,1% · 1,04 | **+82,3%** · 1,81 | SPY +73,6% · 2,19 |
| Riesgoso, acciones arg. | +18,6% · 0,36 | +34,8% · 0,55 | Igual peso **+88,0%** · 1,40 |

Conclusiones:
- El momentum de 12 meses mejora claramente a la regla v0.1.
- En ETFs (moderado), el momentum de 12 meses rinde casi lo mismo que el SPY con menos riesgo.
- En acciones argentinas, elegir por momentum fue mucho peor que tener la canasta. Por eso ahora se elige por liquidez y se diversifica.
- Son 4 años de historia en un período muy particular (devaluación de 2023 y rally posterior). Tomarlo como evidencia débil, no como garantía.

## 8. Limitaciones conocidas

- **Flujos de los hard dollar:** están cargados a mano según las condiciones del canje 2020 (solo AL29/GD29/AL30/GD30). Hay que verificarlos contra el prospecto.
- **TIR real de los CER:** cerca del vencimiento distorsiona por el rezago del CER, por eso se descartan los que vencen en menos de 30 días.
- **BYMA:** no responde desde los servidores de GitHub (fuera de Argentina), así que no se usa.
- **Fuentes gratuitas:** pueden tener demoras o caídas, y el informe muestra el estado de cada una.

## 9. Próximas mejoras propuestas

1. **Noticias con sentimiento** como filtro duro: no comprar un CEDEAR con balance en los próximos 5 días. Hoy solo se avisa en el mail.
2. **Rebalanceo y stop de pérdidas** en la cartera simulada, no solo aportes.
3. **Duales y TAMAR** como bucket propio para el perfil conservador.
4. **Comisiones de IEB** cuando migres (un parámetro).
5. **Métricas de riesgo de la cartera propuesta:** duration promedio, exposición a dólar y a inflación.

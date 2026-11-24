# Reglas del detector (v0.1, demo)

Todas las reglas viven en [`config/perfiles.yaml`](config/perfiles.yaml). Este documento explica qué hace cada una y por qué.

> Herramienta personal de análisis. No es asesoramiento financiero: la decisión y la ejecución de cada orden son del usuario.

## 1. Universo

| Bucket | Qué es | Cómo se detecta | Cómo se elige |
|---|---|---|---|
| `cer` | Bonos en pesos ajustados por inflación (TZX…, TX…, DICP, PARP) | prefijo del ticker | dentro del horizonte (1–6 meses), **mayor TIR real** (ArgentinaDatos), luego volumen |
| `tasa_fija` | LECAP (S…) y BONCAP (T…) | patrón `S31L6`, `T30J7` | vence dentro del horizonte y mayor volumen |
| `dollar_linked` | Letras atadas al A3500 (D…) | patrón `D30A7` | vence dentro del horizonte y mayor volumen |
| `hard_dollar` | Soberanos en USD (AL/GD), especie en pesos | lista en `universo.yaml` | primero los de menor duration (AL29/GD29/AL30/GD30) |
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

## 3. Ajustes automáticos por contexto macro

1. **CER vs tasa fija.** Se compara la tasa mensual de plazo fijo (TNA promedio / 12) con la última inflación mensual.
   - Tasa real negativa → +15 pp a CER, −15 pp a tasa fija.
   - Tasa real positiva → al revés.
2. **Brecha cambiaria.** Si MEP/oficial − 1 > 15%, se pasan 10 pp de liquidez a dollar linked (solo conservador).

## 4. Score de renta variable

```
momentum = 0,5 × retorno 3m + 0,5 × retorno 6m
score    = momentum / max(volatilidad anual 3m, 10%)
si RSI(14) > 75 → score × 0,5   (sobrecompra)
```

Filtros (descartan, no penalizan):
- **Moderado:** precio arriba de la media de 200 ruedas y volatilidad < 35%.
- **Riesgoso:** volatilidad < 80%.
- **Todos:** volumen diario > $5 M.

## 5. Ejecución realista

- **Comisiones:** Cocos plan base, 0,45% en acciones/CEDEARs y 0,15% en bonos. Se suman IVA sobre la comisión y ~0,08% de derechos de mercado.
- **Cantidades enteras:** bonos y letras cotizan cada 100 VN. Lo que no alcanza para una unidad queda en liquidez.
- **Tamaño de posición:** ticket mínimo de $20.000. Posiciones más chicas, o que excedan el máximo de posiciones, van a liquidez.

## 6. Paper trading (fase de pruebas)

Cada perfil "invierte" $200.000 el primer día hábil de cada mes según la propuesta del día y se valúa a diario. La liquidez rinde la tasa de plazo fijo. Se compara contra:
- **Mismos aportes en dólar MEP:** ¿le ganamos al dólar?
- **Total aportado:** ¿le ganamos a no hacer nada?

## 7. Limitaciones conocidas de la demo

- LECAP, BONCAP y dollar linked se eligen por vencimiento y liquidez, no por TIR, porque falta el pago final de cada letra (ver mejoras).
- Hard dollar se elige por duration fija, no por TIR.
- Los datos son gratuitos (data912, ArgentinaDatos, BCRA): pueden tener demoras o caídas, y el informe muestra el estado de cada fuente.

## 8. Mejoras propuestas (próximas versiones)

1. **TIR de letras y bonos.** Bajar el flujo de fondos de la ficha técnica de BYMA, calcular TIR/TEM de LECAP, BONCAP, DL y hard dollar, y armar la curva. Con eso se elige por **valor relativo** (punto de la curva que paga más que sus vecinos) en lugar de por volumen.
2. **Breakevens.** Inflación implícita (tasa fija vs CER) contra el REM del BCRA, y devaluación implícita (tasa fija vs DL) contra la banda cambiaria. Esa es la señal que usan las mesas para rotar entre CER, tasa fija y DL.
3. **Backtest histórico** de las reglas de renta variable con 3–5 años de historia, comparado contra comprar y mantener SPY o Merval.
4. **Noticias con sentimiento** (Alpha Vantage + diarios) como filtro: no comprar un CEDEAR con resultados en los próximos 5 días ni una acción con noticias muy negativas.
5. **Stop de pérdidas y rebalanceo** mensual de la cartera simulada, no solo aportes.
6. **Ruteo por broker:** cambiar comisiones a IEB cuando migres (un parámetro).

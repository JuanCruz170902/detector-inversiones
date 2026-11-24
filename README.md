# Detector de oportunidades de inversión

Sistema automático que todos los días hábiles baja datos del mercado argentino, los evalúa con reglas por perfil de riesgo (**conservador, moderado, riesgoso**) y propone cómo repartir el monto mensual a invertir entre bonos CER, LECAP/BONCAP, dollar linked, soberanos en dólares, CEDEARs y acciones.

> Proyecto personal de análisis. No es asesoramiento financiero.

**Tablero:** https://juancruz170902.github.io/detector-inversiones/

## Cómo funciona

```
17:45 ART (lun–vie)  GitHub Actions
  ├─ data912 ........ paneles de bonos, letras, acciones, CEDEARs + historia diaria
  ├─ ArgentinaDatos . inflación, dólares, riesgo país, plazo fijo, TIR de bonos CER
  └─ BCRA ........... A3500, CER, TAMAR, BADLAR
        ↓
  src/motor.py  señales macro → reparto por bucket → ranking → propuesta con cantidades y costos
        ↓
  docs/data/latest.json · docs/data/paper.json · reporte.md   (commit automático)
        ↓
  Tablero (GitHub Pages) + resumen diario por mail con noticias (Claude)
```

## Estructura

| Archivo | Qué hace |
|---|---|
| `config/perfiles.yaml` | Reglas: reparto por perfil, ajustes macro, filtros, comisiones del broker |
| `config/universo.yaml` | CEDEARs, acciones y bonos en dólares que se analizan |
| `src/fuentes.py` | Descarga de datos con reintentos |
| `src/metricas.py` | Clasificación de renta fija por ticker y métricas de renta variable (momentum, volatilidad, RSI, SMA200) |
| `src/motor.py` | Señales macro, rankings y armado de la propuesta |
| `src/paper.py` | Cartera simulada mes a mes, con benchmark en dólar MEP |
| `REGLAS.md` | Explicación de cada regla, limitaciones y próximas mejoras |

## Uso local

```bash
pip install -r requirements.txt
python -m src.main                                 # corrida completa
python -m src.main --monto 300000 --perfil riesgoso  # propuesta puntual
python -m pytest -q tests                          # tests sin internet
```

# Detector de oportunidades — 2026-11-24

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- TNA plazo fijo prom. (%): 20.47
- Dólar oficial: 1600.0
- Dólar MEP: 1743.1
- Dólar CCL: 1806.2
- Riesgo país (pb): 1035.0

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cer | TZXA7 | 76311 VN | $ 99.738 | $ 261 |
| dollar_linked | D15E7 | 25 VN | $ 39.600 | $ 104 |
| tasa_fija | T15E7 | 19247 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 30.298 | $ 0 |

Paper trading: valor $ 199.557 sobre $ 200.000 aportados (-0.22%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears_etf | XLF | 1 acciones | $ 50.025 | $ 312 |
| cer | TZXA7 | 30524 VN | $ 39.895 | $ 104 |
| tasa_fija | T15E7 | 25662 VN | $ 39.894 | $ 104 |
| hard_dollar | AL29 | 48 VN | $ 39.293 | $ 103 |
| liquidez | CAUCION/FCI MM |  | $ 30.269 | $ 0 |

Paper trading: valor $ 199.376 sobre $ 200.000 aportados (-0.31%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| acciones_arg | TXAR | 112 acciones | $ 79.184 | $ 494 |
| cedears | MSFT | 1 acciones | $ 29.420 | $ 184 |
| cedears | CVX | 1 acciones | $ 23.450 | $ 146 |
| cedears | WMT | 2 acciones | $ 26.320 | $ 164 |
| tasa_fija | T15E7 | 19247 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 10.637 | $ 0 |

Paper trading: valor $ 198.933 sobre $ 200.000 aportados (-0.53%); mismos aportes en MEP: $ 200.000.

## Estado de fuentes

- argdatos_inflacion: ok
- argdatos_plazo_fijo: ok
- argdatos_dolares: ok
- argdatos_riesgo_pais: ok
- argdatos_bonos_cer: ok
- bcra: ok
- data912_mep: ok
- data912_bonos: ok
- data912_letras: ok
- data912_ons: ok
- data912_acciones: ok
- data912_cedears: ok
- data912_historia: ok

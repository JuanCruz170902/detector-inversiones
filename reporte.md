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
| dollar_linked | D15E7 | 25 VN | $ 39.662 | $ 104 |
| tasa_fija | T15E7 | 19247 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 30.235 | $ 0 |

Paper trading: valor $ 199.634 sobre $ 200.000 aportados (-0.18%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cer | TZXA7 | 30524 VN | $ 39.895 | $ 104 |
| tasa_fija | T15E7 | 25662 VN | $ 39.894 | $ 104 |
| hard_dollar | AL29 | 48 VN | $ 39.182 | $ 102 |
| liquidez | CAUCION/FCI MM |  | $ 80.717 | $ 0 |

Paper trading: valor $ 199.671 sobre $ 200.000 aportados (-0.16%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T15E7 | 19247 VN | $ 29.921 | $ 78 |
| acciones_arg | TXAR | 37 acciones | $ 26.104 | $ 163 |
| acciones_arg | ALUA | 31 acciones | $ 26.257 | $ 164 |
| liquidez | CAUCION/FCI MM |  | $ 117.313 | $ 0 |

Paper trading: valor $ 199.923 sobre $ 200.000 aportados (-0.04%); mismos aportes en MEP: $ 200.000.

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

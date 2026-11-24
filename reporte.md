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
| cer | TZXA7 | 61002 VN | $ 79.791 | $ 209 |
| dollar_linked | D15E7 | 25 VN | $ 39.600 | $ 104 |
| tasa_fija | S29E7 | 28058 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 50.298 | $ 0 |

Paper trading: valor $ 199.640 sobre $ 200.000 aportados (-0.18%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cedears_etf | XLF | 1 acciones | $ 50.100 | $ 313 |
| cer | TZXA7 | 30501 VN | $ 39.895 | $ 104 |
| tasa_fija | S29E7 | 37411 VN | $ 39.895 | $ 104 |
| hard_dollar | AL29 | 48 VN | $ 39.245 | $ 103 |
| liquidez | CAUCION/FCI MM |  | $ 30.241 | $ 0 |

Paper trading: valor $ 199.442 sobre $ 200.000 aportados (-0.28%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Plazo fijo rinde 1.71% mensual vs inflación 2.20% → tasa real NEGATIVA: conviene CER.
- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| acciones_arg | TXAR | 70 acciones | $ 49.385 | $ 308 |
| cedears | MSFT | 1 acciones | $ 29.640 | $ 185 |
| cedears | CVX | 1 acciones | $ 23.450 | $ 146 |
| cedears | WMT | 2 acciones | $ 26.180 | $ 163 |
| tasa_fija | S29E7 | 28058 VN | $ 29.921 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 40.542 | $ 0 |

Paper trading: valor $ 198.851 sobre $ 200.000 aportados (-0.57%); mismos aportes en MEP: $ 200.000.

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

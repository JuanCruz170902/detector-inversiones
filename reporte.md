# Detector de oportunidades — 2026-11-24

> Herramienta personal de análisis. No es asesoramiento financiero.

## Contexto macro

- Inflación último mes (%): 2.2
- Dólar oficial: 1600.0
- Dólar MEP: 1743.1
- Dólar CCL: 1806.2
- Riesgo país (pb): 1035.0

## Perfil conservador

Preservar poder de compra en pesos con riesgo bajo. Sin acciones.

- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cer | TZXD6 | 21824 VN | $ 69.815 | $ 183 |
| tasa_fija | T15E7 | 38495 VN | $ 59.842 | $ 156 |
| dollar_linked | D15E7 | 25 VN | $ 39.588 | $ 104 |
| liquidez | CAUCION/FCI MM |  | $ 30.313 | $ 0 |

Paper trading: valor $ 199.557 sobre $ 200.000 aportados (-0.22%); mismos aportes en MEP: $ 200.000.

## Perfil moderado

Mayormente renta fija, con una parte en dólares y CEDEARs de índices.

- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| cer | TZXD6 | 12471 VN | $ 39.895 | $ 104 |
| tasa_fija | T15E7 | 25663 VN | $ 39.894 | $ 104 |
| hard_dollar | AL29 | 48 VN | $ 39.202 | $ 103 |
| liquidez | CAUCION/FCI MM |  | $ 80.698 | $ 0 |

Paper trading: valor $ 199.689 sobre $ 200.000 aportados (-0.16%); mismos aportes en MEP: $ 200.000.

## Perfil riesgoso

Busca retorno en renta variable; acepta caídas fuertes.

- Brecha MEP/oficial 8.9%.
- Riesgo país 1035 pb.

Propuesta para $ 200.000:

| Bucket | Instrumento | Cantidad | Monto | Costo |
|---|---|---|---|---|
| tasa_fija | T15E7 | 19247 VN | $ 29.920 | $ 78 |
| liquidez | CAUCION/FCI MM |  | $ 170.001 | $ 0 |

Paper trading: valor $ 199.922 sobre $ 200.000 aportados (-0.04%); mismos aportes en MEP: $ 200.000.

## Estado de fuentes

- argdatos_inflacion: ok
- argdatos_plazo_fijo: error: Fallo https://api.argentinadatos.com/v1/finanzas/tasas/plazo-fijo: 404 Client Error: Not Found for url: https://api.argentinadatos.com/v1/finanzas/tasas/plazo-fijo
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

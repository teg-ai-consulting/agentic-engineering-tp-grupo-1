# Esperado — review-02-n1-listado

## Importante (2)

- **`fragmento.py:19` — N+1 en un listado.** Una query a `items_cache` por cada
  compra. Cita: `REVIEW.md` §regla del incidente + convenciones §Rendimiento.
  Arreglo: batch (`WHERE id IN (...)`) o denormalizar `item_titulo` en `compras`.
- **`fragmento.py:10` — IDOR.** `usuario_id` sale del query param, no del token.
  Cualquiera lee las compras de cualquiera. Cita: ADR-0005 (OWASP A01).

## No debería

- Ignorar el N+1 (es la regla que nació del incidente).
- Ignorar el IDOR o bajarlo a Nit.

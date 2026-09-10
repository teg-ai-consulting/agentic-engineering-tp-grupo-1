---
name: mover-card
description: >-
  Mueve una card de Trello a la columna que corresponde según el estado del
  pipeline. Usar cuando un agente termina un paso (review, qa, dev) y hay que
  reflejarlo en el tablero.
---

El tablero tiene 4 columnas: **To-Do · In Progress · QA · Done**. Los nombres
exactos salen de la variable de repo (no los hardcodees); resolvé nombre → ID
con `get_lists` sobre el board de `TRELLO_BOARD_ID`.

## Mapa estado → columna

| Estado | Columna |
|---|---|
| card recién tomada por el pipeline | `In Progress` |
| el `qa` arranca | `QA` |
| `qa` PASS / `revisor` LIMPIO o OBSERVA | `Done` |
| feature **o** fix: PR abierto y CI verde | `Done` |
| **incidente**: diagnóstico + ADR borrador + test rojo listos | `QA` + etiqueta `revisión-adr` (espera el gate humano) |
| incidente que un humano marcó `aprobado-para-fix` (ya se creó la card de fix) | `Done` |
| incidente que un humano marcó `descartado` (ya se comentó el motivo) | `Done` |
| **pull-back**: `qa` FAIL, o `revisor` BLOQUEA, o un gatekeeper rechaza | `In Progress` + etiqueta `bloqueado` |

## Reglas duras

- **Nunca** movés una card a `Done` sin que el `qa` haya corrido.
- **Nunca** movés un **incidente** a `Done` hasta que un humano haya puesto
  `aprobado-para-fix` o `descartado`. Sin decisión, se queda en `QA` con
  `revisión-adr`.
- **Nunca** movés más allá de `Done`. El merge y el deploy los dispara un humano
  y quedan como comentarios (skill `registrar-en-card`), no como columna.
- Si la card ya está en `Done` y llega un pull-back, movela a `In Progress` y
  sacale cualquier etiqueta de cierre.

Detalle de payloads y ejemplos: [`ejemplos.md`](ejemplos.md).

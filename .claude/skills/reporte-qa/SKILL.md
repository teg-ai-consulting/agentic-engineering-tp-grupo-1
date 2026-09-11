---
name: reporte-qa
description: >-
  Formatea el reporte del `qa` (pruebas realizadas, cobertura por criterio,
  fallos con hipótesis de causa, veredicto), lo publica en Confluence (skill
  `publicar-en-confluence`) y deja el detalle + la transición correspondiente
  en la card de Trello (skill `mover-card`). Usarla solo desde el agente `qa`,
  al cierre de su análisis. No decide el veredicto ni corrige nada: solo
  publica lo que el `qa` ya resolvió.
---

El que lee la card tiene que poder entender, sin abrir el repo, qué se probó,
qué falló y por qué se cree que falló — no solo "hay un bug".

## Antes de publicar nada

No comentés a medias. Antes de llamar a esta skill tenés que tener:

- **veredicto** (`PASS` / `FAIL`) ya decidido.
- **cobertura por criterio**: qué test cubre cada criterio de aceptación.
- si es `FAIL`: **cada fallo** con entrada usada / esperado vs. obtenido /
  hipótesis de causa (y `archivo:línea` cuando se pueda).
- `pytest -q` corrido de verdad — no se supone el resultado.

Si falta algo de esto, volvé al agente `qa` y completá el análisis primero.

## 1. Confluence (skill `publicar-en-confluence`)

Publicá el reporte completo (resumen, cobertura, fallos, veredicto) bajo la
página del grupo. Título: `QA — <feature o slug> — <fecha ISO>`. Guardá la
URL — va en el comentario de Trello del paso 3.

Si Confluence no responde: seguí igual, anotá en el comentario de Trello
"Confluence no disponible — reporte solo en el repo".

## 2. Mover la card (skill `mover-card`)

| Momento | Movimiento |
|---|---|
| al empezar el análisis | `In Progress` → `QA` |
| veredicto `PASS` | se queda en `QA` — el `documentador` la cierra a `Done` cuando también `revisor` dé OK y el PR esté abierto |
| veredicto `FAIL` | `QA` → `In Progress` + etiqueta `bloqueado` |

## 3. Comentario en la card

```
[qa] <PASS|FAIL> — N tests, N pasan, N fallan

Cobertura:
· <criterio 1> — cubierto por <test>
· <criterio 2> — cubierto por <test>

Fallos (si FAIL):
· entrada: <valor usado>
  esperado: <...> / obtenido: <...>
  hipótesis: <por qué creemos que falla — archivo:línea si se puede>

reporte: <link de Confluence, o "solo en el repo" si no publicó>
```

Ejemplo (`FAIL`):

```
[qa] FAIL — 7 tests, 6 pasan, 1 falla

Cobertura:
· listado paginado devuelve cursor válido — cubierto por test_listado_items_paginado
· listado no hace N+1 al traer vendedor — cubierto por test_listado_items_sin_n1

Fallos:
· entrada: GET /v1/items?limit=20
  esperado: 1 query para los 20 vendedores / obtenido: 20 queries (1 por item)
  hipótesis: no se batchea el fetch de vendedor en items-service/routers/items.py:42 —
  sigue resolviendo uno por uno en el loop de serialización.

reporte: https://<confluence>/QA-listado-items-2026-09-11
```

Ejemplo (`PASS`):

```
[qa] PASS — 7 tests, 7 pasan, 0 fallan

Cobertura:
· listado paginado devuelve cursor válido — cubierto por test_listado_items_paginado
· listado no hace N+1 al traer vendedor — cubierto por test_listado_items_sin_n1
· ... (5 más)

reporte: https://<confluence>/QA-listado-items-2026-09-11
```

## Reglas

- Un comentario por análisis, no editás comentarios viejos.
- El detalle de un fallo tiene que alcanzar para que el desarrollador lo
  reproduzca sin volver a correr toda la suite él mismo.
- Si Trello no responde: dejá el reporte igual (Confluence + repo), anotá en
  la salida qué no se pudo publicar, y seguí. La observabilidad es un
  nice-to-have sobre el pipeline, no un bloqueante.

## Qué NO hace esta skill

- No decide el veredicto ni redacta los fallos — eso ya lo resolvió el `qa`
  antes de llamarla. Esta skill solo formatea y publica.
- No mueve la card más allá de `QA`/`In Progress` — el salto a `Done` es del
  `documentador`, no de esta skill.
- No pone ni saca los labels de gate humano (`aprobado-para-fix`,
  `descartado`) — esos son exclusivos del board, por `GOBERNANZA.md`.
- No corrige el código que falló. El `qa` reporta; `desarrollador-backend` /
  `desarrollador-frontend` corrigen.

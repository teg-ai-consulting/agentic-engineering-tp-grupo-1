---
name: crear-card
description: >-
  Crea una card nueva en Trello, en la columna To-Do, con su label de tipo y un
  body autocontenido. La usa el guardia cuando un incidente aprobado se convierte
  en una card `tipo: fix`. No la uses para reflejar un paso del pipeline (eso es
  mover-card / registrar-en-card).
---

El guardia crea una sola clase de card: la de **fix**, a partir de un incidente
que un humano marcó `aprobado-para-fix` (ver `GOBERNANZA.md` y
`guardia/guardia-prompt.md` §3). Nunca crees una card de tu propia iniciativa.

## Cómo

```
set_active_board(board_id = <TRELLO_BOARD_ID>)
listas  = get_lists()
todo    = next(l.id for l in listas if l.name == "To-Do")
add_card(list_id = todo, name = <título del ADR>, desc = <body>)
# resolvé "tipo: fix" nombre → id como las listas y agregá el label a la card
```

El nombre exacto de la tool (`add_card`, `add_card_to_list`, ...) es del servidor
MCP de Trello — verificalo contra su README.

## El body tiene que ser autocontenido

El run que va a tomar la card `tipo: fix` arranca **sin contexto**. El body
lleva todo:

```
Alternativa aprobada: <batch-load ?ids= | denormalizar vendedor_nombre>

<qué cambiar, pegado del ADR: archivo(s), servicio, endpoint>
<límite de pool si aplica>

Aceptación: test_incidente_listado.py pasa a verde; el resto sigue verde.

ADR: <link Confluence>
Incidente original: <link a la card>
@<owner>
```

## Reglas

- Solo a `To-Do`. Nunca creás una card ya en `In Progress` o más allá.
- Una card de fix por incidente aprobado. Si ya existe (buscá por título), no
  dupliques: comentá el link y seguí.
- El label `tipo: fix` es obligatorio — es lo que hace que el guardia la procese
  por el flujo de implementación y no como incidente.

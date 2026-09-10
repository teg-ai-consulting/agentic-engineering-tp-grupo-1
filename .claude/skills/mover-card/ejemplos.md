# mover-card — ejemplos

## Resolver la columna

```
set_active_board(board_id = <TRELLO_BOARD_ID>)
listas = get_lists()          # [{id, name}, ...]
destino = next(l.id for l in listas if l.name == "QA")
move_card(card_id = <id>, list_id = destino)
```

## Pull-back con etiqueta

```
move_card(card_id, list_id = <In Progress>)
# agregar la etiqueta "bloqueado" (por nombre → id, como las listas)
add_comment(card_id, "QA FAIL — vuelve a In Progress. Fallos: ...")
```

## Qué NO hacer

- `move_card(..., "Aprobado")` — no existe esa columna. El gate humano no es una
  columna.
- Mover a `Done` desde `In Progress` salteando `QA`.
- Hardcodear `"To-Do"` / `"QA"` si el board del grupo los nombró distinto — por
  eso se resuelve con `get_lists` y la variable del repo.

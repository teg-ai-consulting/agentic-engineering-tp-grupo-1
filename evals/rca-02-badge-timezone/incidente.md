# Incidente rca-02

Tras el deploy de la feature "badge NOVEDAD", **todos** los items del home
muestran el badge NOVEDAD, incluso los publicados hace meses. Sin errores, sin
latencia — solo el badge mal.

El badge se calcula en el frontend: `(Date.now() - Date.parse(item.publicado_en)) / 86400000 <= 3`.
`item.publicado_en` llega como `"2026-07-01 08:00:00"` (sin `Z`, sin offset).
El deploy incluyó un bump de la lib de fechas; la versión nueva parsea los
strings sin timezone como **hora local** en vez de UTC, y el server corre en
UTC-3 → todo se corre 3h... no, peor: algunos entornos lo interpretan como
epoch-relativo y `Date.parse` devuelve `NaN` → la resta da `NaN` → `NaN <= 3`
es `false`... salvo en Safari, donde el string sin `Z` tira `Invalid Date` y el
fallback muestra el badge siempre.

`GET /v1/items/{id}` devuelve `publicado_en` con el mismo formato sin `Z`.

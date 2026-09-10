# Incidente rca-01 (= el de la Parte 1, para el eval)

`GET /v1/items` p99 200ms → 8s en horario pico (promo x5 tráfico). p50 estable.
`GET /v1/items/{id}` sin cambios. `items_db` con 20/20 conexiones, 47 en cola.
`vendedores_db` QPS x18, queries triviales `WHERE id = $1` < 3ms cada una.
El código del listado no se tocó en meses. Se recupera solo al bajar el tráfico.

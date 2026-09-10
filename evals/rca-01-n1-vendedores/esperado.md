# Esperado — rca-01-n1-vendedores

## Síntoma

`GET /v1/items` timeoutea **solo bajo carga**; p50 ok, p99 explota. El listado,
no el detalle. La base de items con el pool lleno.

## Causa raíz

El listado hace un `SELECT` a `vendedores` **por cada item** de la página (N+1).
Con tráfico normal se banca; con x5, son miles de queries chiquitas concurrentes
que agotan el pool de conexiones. Cita: convenciones §Rendimiento ("sin N+1 en
listados"), ADR-0001 (lecturas cruzadas en batch).

## Clasificación

**Lógica** (el N+1) que **bajo carga** se comporta como **entorno/infra** (pool
agotado). Nombrar las dos, no elegir una a ciegas.

## No debería

- "Contrato roto" — ningún contrato cambió.
- "Escalar más réplicas" como causa/solución (es lo que dice el comentario de la
  card; es un parche, no la causa).
- Clasificar solo como "entorno/infra" sin mencionar el N+1.

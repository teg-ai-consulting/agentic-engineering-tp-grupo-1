# Snapshot de métricas — items-service — 2026-09-20

## Timeline

| Hora UTC | Evento |
|---|---|
| 20:30 | arranca la promo "Semana del Envío Gratis" |
| 20:35 | tráfico a `GET /v1/items` sube de ~400 rpm a ~2.000 rpm |
| 20:45 | autoscaling: items-service 3 → 8 réplicas. Sin mejora. |
| 20:52 | p99 de `GET /v1/items` cruza 3s |
| 21:07 | PagerDuty P1 |
| 22:40 | cae el tráfico de la promo, se normaliza solo |

## Dashboards

- `GET /v1/items` — p50 estable (~200ms), **p99 explota** (200ms → 8s).
- `GET /v1/items/{id}` — sin cambios. **Solo el listado se degrada.**
- CPU de items-service: 40% (no es CPU).
- `items_db`: conexiones activas 20/20 (tope), 47 en cola. **Es la base.**
- `vendedores_db`: QPS x18 respecto del baseline. Queries triviales
  (`WHERE id = ...`), todas < 3ms individualmente, pero muchísimas.

## Cambios recientes (últimas 3 semanas)

| Fecha | Deploy | Servicio |
|---|---|---|
| 2026-09-11 | bump de dependencias (rutina) | items-service |
| 2026-08-30 | nuevo endpoint `GET /v1/vendedores?ids=` (batch) | vendedores-service |

**El listado no se tocó.** El código de `GET /v1/items` que corre hoy es el
mismo desde hace meses — la query por-vendedor siempre estuvo. Lo que cambió es
el tráfico. Ver `prod/deploy-log.jsonl`.

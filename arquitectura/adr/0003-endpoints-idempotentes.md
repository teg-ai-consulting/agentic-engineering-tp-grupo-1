# ADR-0003 — Endpoints de escritura idempotentes

- **Estado:** aceptado
- **Fecha:** 2026-05-24

## Contexto

Reintentos de red y doble-click generan órdenes o publicaciones duplicadas.

## Decisión

Todo `POST`/`PUT` que crea o modifica estado acepta el header
**`Idempotency-Key`** (UUID que genera el cliente). El servidor guarda el
resultado de la primera ejecución con esa key y devuelve el mismo resultado ante
un reintento con la misma key, sin volver a ejecutar el efecto.

## Consecuencias

- `POST /v1/compras` sin `Idempotency-Key` → `400`.
- La tabla de idempotencia se limpia con TTL (24 h).

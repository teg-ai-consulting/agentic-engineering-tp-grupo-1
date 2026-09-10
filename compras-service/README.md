# compras-service

**No existe todavía.** Lo construye la feature "Mis compras" (Parte 2), backlog
del PO. Contrato propuesto: `../arquitectura/openapi/compras-service.yaml`.

Cuando la factory lo cree: `GET /v1/compras` filtra por `token.sub` (ADR-0005),
`POST /v1/compras` requiere `Idempotency-Key` (ADR-0003).

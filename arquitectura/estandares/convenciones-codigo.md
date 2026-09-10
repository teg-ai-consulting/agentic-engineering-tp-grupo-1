# Convenciones de código — Marketplace

Reglas obligatorias para todo servicio nuevo o modificado. Un PR que no las
cumple no se mergea.

## Python (FastAPI)

- Python 3.12, `ruff` para lint y formato, `mypy` estricto.
- **Type hints obligatorios** en toda función pública.
- DTOs con **Pydantic v2** (`model_config = ConfigDict(extra="forbid")`).
- `snake_case` funciones/variables, `PascalCase` clases.
- Un router por recurso en `app/routers/<recurso>.py`.
- Tests con **pytest**; cada endpoint nuevo trae happy path + un caso de error.

## Contratos HTTP

- Versionado en la ruta: `/v1/...`.
- Errores en **RFC 7807** (`application/problem+json`): `type`, `title`,
  `status`, `detail`, `instance`.
- **Paginación por cursor**, nunca por `offset`. `?cursor=<opaco>&limit=<n>`,
  respuesta con `items` y `next_cursor` (null si no hay más).
- Fechas/horas: **ISO 8601 en UTC** siempre (`2026-09-01T13:45:00Z`).
- Campos JSON en `snake_case`.

## Rendimiento

- **Sin N+1 en listados.** Un endpoint que devuelve una lista **no** hace una
  query por elemento para traer datos relacionados. Batch (`WHERE id IN (...)`)
  o denormalización.
- Toda conexión a la base sale de un **pool con límite explícito**.

## Dinero

- **Enteros en centavos** (ARS). Nunca `float`.
- Todo importe viaja con su moneda: `{ "importe": 125000, "moneda": "ARS" }`.

## Imágenes y archivos

- Ver [ADR-0004](../adr/0004-imagenes-url-object-storage.md): las imágenes se
  guardan en **object storage** y en la base va solo la **URL**. Nunca binario
  ni base64 en una columna.

## Comunicación entre servicios

- Ver [ADR-0001](../adr/0001-comunicacion-entre-servicios.md): eventos primero;
  las lecturas cruzadas por la **API REST del servicio dueño**, jamás contra su
  base.

## Autorización

- Ver [ADR-0005](../adr/0005-autorizacion-por-dueno-del-dato.md): todo endpoint
  que devuelve datos de un usuario valida que el **token** sea de ese usuario.
  Nunca confiar en un `usuario_id` que venga en el request.

## Idempotencia

- Ver [ADR-0003](../adr/0003-endpoints-idempotentes.md): todo `POST`/`PUT` que
  cree o modifique estado acepta y respeta `Idempotency-Key`.

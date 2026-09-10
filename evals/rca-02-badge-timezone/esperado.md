# Esperado — rca-02-badge-timezone

## Síntoma

El badge NOVEDAD aparece en todos los items tras el deploy. Sin errores ni
latencia. Solo lógica de presentación.

## Causa raíz

`publicado_en` se sirve **sin timezone** (`"2026-07-01 08:00:00"`, sin `Z`),
violando la convención "ISO 8601 en UTC siempre". El cálculo del badge en el
front depende de un parseo ambiguo que la lib nueva cambió. La causa está en el
**contrato del campo** (formato de fecha), no en la lib.

Cita: convenciones §Contratos HTTP ("Fechas/horas: ISO 8601 en UTC siempre").

## Clasificación

**Lógica con un caso borde** — el código nunca contempló un `publicado_en` sin
`Z` (aunque la convención lo exige). El bump de lib fue el disparador, no la
causa.

## No debería

- **"Entorno/infra"** — no es el pool ni la infra, es el formato del dato.
- "Contrato roto entre servicios" — es el mismo servicio sirviendo mal un campo.
- "Revertir la lib" como única medida — el formato sin `Z` sigue mal.
- Si el pipeline dice "N+1" acá, está pegando el caso rca-01 a todo → FAIL.

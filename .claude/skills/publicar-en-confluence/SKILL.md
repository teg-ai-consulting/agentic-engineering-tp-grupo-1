---
name: publicar-en-confluence
description: >-
  Publica un documento markdown (ADR propuesto, diagnóstico de incidente) como
  página de Confluence bajo la página del grupo. Devuelve el link. Usar cuando
  el pipeline produce un doc que el equipo lee fuera del repo.
---

## Dónde

- Espacio y página padre salen de las variables del repo:
  `CONFLUENCE_SPACE` y `CONFLUENCE_PARENT_PAGE_ID`.
- Título: `<TIPO> — <slug> — <fecha ISO>` (ej. `ADR propuesto — n1-vendedores — 2026-09-22`).

## Cómo

1. `confluence_get_page(CONFLUENCE_PARENT_PAGE_ID)` para confirmar que existe.
2. `confluence_create_page(space=..., parent_id=CONFLUENCE_PARENT_PAGE_ID,
   title=..., body=<markdown o storage format>)`.
3. Guardá la URL que devuelve. Va en el comentario de Trello (skill
   `registrar-en-card`) y en la salida del agente.

## Reglas

- El doc también queda en el repo (`docs/`). Confluence es una **copia
  publicada**, no la fuente de verdad.
- Un ADR propuesto se publica marcado **BORRADOR — pendiente de aprobación
  humana**.
- Si el MCP de Confluence no responde (sin red en CI, token mal): NO falla el
  pipeline. Dejá el doc en `docs/`, registrá en Trello "Confluence no disponible
  — link pendiente", y seguí.

## Nota

Los nombres de tool (`confluence_create_page`, ...) son del MCP de la comunidad
`mcp-atlassian`. Si usás el oficial de Atlassian, cambian — verificá contra su
doc (ver `CONFIGURACION.md`).

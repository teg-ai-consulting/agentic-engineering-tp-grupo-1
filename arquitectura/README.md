# Arquitectura de ejemplo — Marketplace

Genérica y ficticia. Es lo que el `arquitecto`, el `revisor` y el `investigador`
citan cuando marcan una violación de diseño.

| Carpeta | Qué hay |
|---|---|
| `catalogo-servicios.json` | los 5 servicios, quién expone/consume qué |
| `estandares/convenciones-codigo.md` | reglas obligatorias (HTTP, dinero, rendimiento, imágenes, auth) |
| `adr/` | 6 ADR — las decisiones que un PR no puede violar |
| `openapi/` | contratos de `items-service` y `compras-service` |

Los agentes la leen **directo del repo** (está en el checkout). Si querés
exponerla por MCP como en la Clase 3, apuntá tu servidor `arquitectura` a esta
carpeta — es opcional.

**En tu organización:** reemplazá esto por tu catálogo, tus ADR y tus OpenAPI
reales.

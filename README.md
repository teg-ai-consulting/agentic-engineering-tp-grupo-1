# codigo-inicial — Marketplace

El repo que cada grupo publica en GitHub. Mínimo y runnable.

## Servicios

| Carpeta | Qué es |
|---|---|
| `items-service/` | `GET /v1/items` (cursor) + `/v1/items/{id}`. **Trae el N+1 del incidente.** |
| `vendedores-service/` | stub. Tiene el endpoint batch `GET /v1/vendedores?ids=` (el que habilita el fix). |
| `usuarios-service/` | stub. Login → JWT con `sub`. |
| `compras-service/` | no existe — lo construye la feature "Mis compras". |
| `web/index.html` | frontend: lista items. |

## Pipeline

| Archivo | Qué es |
|---|---|
| `REVIEW.md` | política de review — completa, se lee y la aplica el `revisor` |
| `.claude/agents/` | los 7 agentes — el `qa` lo escribís vos |
| `.claude/skills/` | `mover-card`, `registrar-en-card`, `publicar-en-confluence`, `crear-card` + tu `reporte-qa` y `ticket-po` |
| `.claude/settings.json` + `.claude/hooks/` | git-guard + lint post-edit |
| `.mcp.json` | Trello + Confluence + Slack |
| `.github/workflows/` | `ci.yml`, `claude-review.yml`, `deploy.yml`, `guardia.yml`, `evals.yml` (prompts hechos) |
| `GOBERNANZA.md` | matriz de autonomía del guardia |
| `guardia/guardia-prompt.md` | el orquestador programado |
| `evals/` | casos con resultado conocido |
| `incidente/` | evidencia del incidente (Parte 2) |
| `prod/deploy-log.jsonl` | "entorno" del deploy stub |

## Correr local

```bash
pip install fastapi httpx pytest ruff
cd items-service && python -m pytest -q                       # verde
cd .. && python -m pytest -q incidente/regresion_referencia.py  # FALLA: el N+1
python items-service/main.py                                  # :8001
```

Enunciado: [`../../../clase-5/proyecto-final.md`](../../../clase-5/proyecto-final.md).
Infra: [`../../CONFIGURACION.md`](../../CONFIGURACION.md).

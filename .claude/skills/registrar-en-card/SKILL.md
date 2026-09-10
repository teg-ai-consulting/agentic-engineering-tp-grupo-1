---
name: registrar-en-card
description: >-
  Registra un evento del pipeline como comentario estructurado en la card de
  Trello y adjunta los artefactos. Es la capa de observabilidad: cada paso deja
  rastro. Usar cada vez que algo relevante ocurre (CI, review, qa, merge, deploy,
  diagnóstico).
---

La card acumula un **trail**: un comentario por evento, en orden. Alguien que
mira la card entiende qué pasó sin abrir GitHub.

## Formato del comentario

```
[<paso>] <resultado en una línea>
· <dato clave 1>
· <dato clave 2>
<link si aplica>
```

Ejemplos:

```
[CI] verde — 4 tests, 0.6s

[review] BLOQUEA — 1 Importante, 3 Nit
· badge calculado en el front con parseo ambiguo de fecha (convenciones §Contratos HTTP)
adjunto: hallazgos.md

[qa] PASS — 7 tests
reporte: https://<confluence>/QA-badge-novedad

[deploy] ok — prod/deploy-log.jsonl entrada e7f8g9h

[diagnóstico] causa raíz: N+1 a vendedores en GET /v1/items (convenciones §Rendimiento)
clasificación: lógica → entorno/infra bajo carga
adjunto: diagnostico-listado.md
```

## Reglas

- Un comentario por evento, no editás comentarios viejos (el trail es
  cronológico).
- Adjuntá el artefacto que respalda el evento (`hallazgos.md`, `diagnostico-*.md`,
  la salida de `pytest`).
- Si Trello no responde: log local + seguí. La observabilidad es un nice-to-have
  sobre el pipeline, no un bloqueante.

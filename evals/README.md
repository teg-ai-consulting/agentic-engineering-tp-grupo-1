# Evals del pipeline

Casos con resultado conocido. `evals.yml` los corre cuando alguien toca los
agentes, `REVIEW.md` o el guardia. Si la detección baja o la clasificación
deriva → FAIL → no se mergea el cambio.

| Caso | Tipo | Qué prueba |
|---|---|---|
| `review-01-ssrf` | review | fetch de URL de tercero → Importante (OWASP A10) |
| `review-02-n1-listado` | review | query por item en un listado → Importante (regla del incidente) |
| `rca-01-n1-vendedores` | rca | el incidente del listado → clasificación "lógica → entorno/infra", cita convenciones §Rendimiento |
| `rca-02-badge-timezone` | rca | badge NOVEDAD en todos los items → "lógica con caso borde", **no** "entorno/infra" |

`rca-02` existe para detectar sobre-generalización: si el pipeline clasifica todo
como el caso que ya vio, falla.

Cada caso: los archivos de entrada + `esperado.md`.

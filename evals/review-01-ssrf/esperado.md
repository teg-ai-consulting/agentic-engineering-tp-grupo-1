# Esperado — review-01-ssrf

## Importante (1)

- **`fragmento.py:11` — SSRF.** `requests.get(url)` sobre una URL arbitraria que
  manda el cliente. Permite pegarle a `169.254.169.254`, servicios internos,
  etc. Cita: OWASP A10:2021 + ADR-0004 ("el servicio no descarga la URL de un
  tercero; allowlist de hosts propios"). Arreglo: validar contra la allowlist
  del bucket, o no bajar la imagen.

## Nit

- `body: dict` en vez de un modelo Pydantic (convenciones). Defendible como Nit.

## No debería

- Bajarlo a Nit "validación de input". Es Importante.

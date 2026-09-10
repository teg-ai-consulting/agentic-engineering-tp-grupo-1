# ADR-0004 — Imágenes: URL a object storage, nunca binario en la base

- **Estado:** aceptado
- **Fecha:** 2026-06-14

## Contexto

Las fotos de los items pesan. Guardarlas en la base (BLOB o base64 en una
columna `text`) infla las filas, rompe el rendimiento de los listados y hace
inmanejables los backups.

## Decisión

1. El binario de la imagen vive en **object storage** (S3-compatible). La base
   guarda solo la **URL** (y metadata: `ancho`, `alto`, `content_type`).
2. El servicio **no descarga ni re-hostea** la URL que manda un tercero. Si
   necesita validar la imagen, lo hace contra una **allowlist de hosts** propios
   (el bucket del marketplace), nunca haciendo un `GET` a una URL arbitraria del
   vendedor — eso es SSRF.
3. La subida es: el cliente pide una **URL prefirmada** al servicio, sube
   directo al bucket, y manda al servicio la URL final.

## Consecuencias

- La tabla `items` tiene `foto_url text` (o una tabla `item_fotos` con URLs),
  nunca `foto_bytes`.
- Un endpoint que reciba una URL de imagen de afuera y le haga `requests.get()`
  es un hallazgo Importante.

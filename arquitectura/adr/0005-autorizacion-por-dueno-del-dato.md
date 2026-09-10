# ADR-0005 — Autorización: el dueño del dato sale del token, no del request

- **Estado:** aceptado
- **Fecha:** 2026-07-02

## Contexto

Un endpoint que devuelve datos de un usuario (`GET /v1/compras`) tiene que saber
de qué usuario. Tomar el `usuario_id` de un query param o del body es un IDOR
(Insecure Direct Object Reference, OWASP A01): cualquiera pide las compras de
cualquiera.

## Decisión

1. La identidad del usuario que hace el request sale **siempre del JWT**
   (`sub`), validado por el middleware de auth. Nunca de un parámetro del
   request.
2. Un endpoint de datos personales (`/v1/compras`, `/v1/usuarios/me`, ...) filtra
   por el `sub` del token. Si además recibe un `usuario_id`, tiene que
   **coincidir** con el del token o devolver `403`.
3. Los endpoints de datos públicos (`GET /v1/items`, `GET /v1/vendedores/{id}`)
   no tienen esta restricción — no devuelven datos personales.

## Consecuencias

- `GET /v1/compras?usuario_id=...` que confía en el query param es un hallazgo
  Importante (seguridad).
- "Mis compras" filtra por `token.sub`, punto.

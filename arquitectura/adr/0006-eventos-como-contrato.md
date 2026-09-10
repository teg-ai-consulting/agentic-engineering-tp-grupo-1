# ADR-0006 — Los eventos de dominio son un contrato

- **Estado:** aceptado
- **Fecha:** 2026-07-02

## Contexto

Un evento de Kafka no tiene un cliente que "pida" campos: el publisher no sabe
quién consume. Un cambio silencioso rompe consumidores sin aviso.

## Decisión

1. El payload `data` de un tipo de evento (`item.publicado`) es un contrato
   público, documentado en `modelos-datos/`.
2. Cambio **aditivo** (permitido sin versionar): solo agrega campos opcionales.
3. Cambio **breaking** (requiere tipo de evento nuevo, ej. `item.publicado.v2`):
   elimina un campo, vuelve opcional uno obligatorio, o cambia el tipo/forma de
   un campo.
4. El tipo nuevo convive con el viejo durante una ventana acordada con los
   consumidores. Nunca se reemplaza en el mismo topic.

## Consecuencias

- "El consumer asumía un campo que el publisher dejó de mandar" = contrato roto,
  y la culpa es del cambio no versionado, no del consumer.

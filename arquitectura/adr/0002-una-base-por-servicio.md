# ADR-0002 — Una base de datos por servicio

- **Estado:** aceptado
- **Fecha:** 2026-05-10

## Contexto

Compartir una base entre servicios acopla sus esquemas y sus deploys.

## Decisión

Cada servicio es dueño de su base (`items_db`, `vendedores_db`, ...). Ningún
servicio se conecta a la base de otro — ni para leer. El acceso cruzado es por
API REST o por evento (ADR-0001).

## Consecuencias

- Un `JOIN` entre `items` y `vendedores` a nivel base **no existe**. Lo que
  parece un join es un batch-read o un dato denormalizado.

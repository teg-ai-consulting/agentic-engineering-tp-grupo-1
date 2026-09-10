# ADR-0001 — Comunicación entre servicios: eventos primero, lecturas por API REST del dueño

- **Estado:** aceptado
- **Fecha:** 2026-05-10

## Contexto

Los servicios necesitan datos de otros servicios (el listado de items muestra el
nombre del vendedor; "Mis compras" muestra el título del item). Dos anti-patrones
frecuentes: leer directo la base ajena, o encadenar llamadas REST sincrónicas
por elemento.

## Decisión

1. Cambios de estado se propagan por **eventos de dominio** (Kafka, CloudEvents
   1.0). El publisher no sabe quién consume.
2. Una lectura puntual de datos de otro servicio se hace por su **API REST**
   pública, nunca contra su base.
3. Si un endpoint devuelve una **lista** y necesita datos de otro servicio para
   cada elemento, se resuelve en **batch** (un `GET /v1/vendedores?ids=1,2,3`),
   no una llamada por item. Ver la regla "sin N+1 en listados" en las
   convenciones.
4. Datos que se leen mucho y cambian poco (nombre del vendedor) se pueden
   **denormalizar** en el consumer, actualizándolos por evento.

## Consecuencias

- El listado de items no puede depender de N llamadas a `vendedores-service`.
- Cada consumer decide entre batch-read o denormalización según su patrón de
  acceso.

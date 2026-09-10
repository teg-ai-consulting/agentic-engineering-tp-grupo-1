"""items-service — alimenta el listado del home del marketplace.

`GET /v1/items`  — lista paginada por cursor.
`GET /v1/items/{id}` — un item.

Estado: funcional. Trae el bug del incidente de la Parte 1 (ver el README de
codigo-inicial): el listado resuelve el nombre y la reputación del vendedor
con una query POR CADA item (N+1). Con poco tráfico no se nota; bajo carga
satura la base.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="items-service")

# --- infra de DB con contador de queries (para el test de regresión) ----------

_QUERY_COUNT = 0


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    return conn


_CONN = None


def get_db() -> sqlite3.Connection:
    global _CONN
    if _CONN is None:
        _CONN = _connect()
    return _CONN


@contextmanager
def query_counter():
    """Cuenta las queries ejecutadas dentro del bloque. Lo usa el test."""
    start = _QUERY_COUNT
    yield lambda: _QUERY_COUNT - start


def _execute(conn: sqlite3.Connection, sql: str, params: tuple = ()):
    global _QUERY_COUNT
    _QUERY_COUNT += 1
    return conn.execute(sql, params)


# --- endpoints ---------------------------------------------------------------


@app.get("/v1/items")
def listar_items(cursor: str | None = None, limit: int = Query(20, le=100)):
    conn = get_db()
    where = "WHERE id > ?" if cursor else ""
    params = (cursor, limit + 1) if cursor else (limit + 1,)
    filas = _execute(
        conn,
        f"SELECT id, titulo, precio_centavos, moneda, vendedor_id, publicado_en, foto_url "
        f"FROM items {where} ORDER BY id LIMIT ?",
        params,
    ).fetchall()

    tiene_mas = len(filas) > limit
    filas = filas[:limit]

    items = []
    for f in filas:
        # N+1: una query a vendedores por cada item del listado.
        v = _execute(
            conn,
            "SELECT nombre, reputacion FROM vendedores WHERE id = ?",
            (f["vendedor_id"],),
        ).fetchone()
        items.append(
            {
                "id": f["id"],
                "titulo": f["titulo"],
                "precio_centavos": f["precio_centavos"],
                "moneda": f["moneda"],
                "vendedor_id": f["vendedor_id"],
                "vendedor_nombre": v["nombre"] if v else None,
                "vendedor_reputacion": v["reputacion"] if v else None,
                "publicado_en": f["publicado_en"],
                "foto_url": f["foto_url"],
            }
        )

    return {"items": items, "next_cursor": items[-1]["id"] if tiene_mas and items else None}


@app.get("/v1/items/{item_id}")
def obtener_item(item_id: str):
    conn = get_db()
    f = _execute(
        conn,
        "SELECT id, titulo, precio_centavos, moneda, vendedor_id, publicado_en, foto_url "
        "FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()
    if f is None:
        raise HTTPException(status_code=404, detail="item no encontrado")
    v = _execute(
        conn, "SELECT nombre, reputacion FROM vendedores WHERE id = ?", (f["vendedor_id"],)
    ).fetchone()
    return {
        "id": f["id"],
        "titulo": f["titulo"],
        "precio_centavos": f["precio_centavos"],
        "moneda": f["moneda"],
        "vendedor_id": f["vendedor_id"],
        "vendedor_nombre": v["nombre"] if v else None,
        "publicado_en": f["publicado_en"],
        "foto_url": f["foto_url"],
    }


# --- datos de ejemplo -------------------------------------------------------

_SCHEMA = """
CREATE TABLE vendedores (id TEXT PRIMARY KEY, nombre TEXT, reputacion TEXT);
INSERT INTO vendedores VALUES
  ('v1','TiendaTech','verde'), ('v2','HogarYMas','verde'), ('v3','ModaSur','amarillo');

CREATE TABLE items (
  id TEXT PRIMARY KEY, titulo TEXT, precio_centavos INTEGER, moneda TEXT,
  vendedor_id TEXT, publicado_en TEXT, foto_url TEXT
);
INSERT INTO items VALUES
  ('i01','Auriculares BT',  4500000,'ARS','v1','2026-09-06T10:00:00Z',NULL),
  ('i02','Cafetera',        8900000,'ARS','v2','2026-09-05T09:00:00Z',NULL),
  ('i03','Zapatillas run', 12000000,'ARS','v3','2026-08-20T12:00:00Z',NULL),
  ('i04','Teclado mecánico',6200000,'ARS','v1','2026-09-07T14:00:00Z',NULL),
  ('i05','Silla gamer',    31000000,'ARS','v2','2026-07-01T08:00:00Z',NULL);
"""


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

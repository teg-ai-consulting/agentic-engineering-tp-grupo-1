"""PR de ejemplo: 'Mis compras' — listar las compras del usuario con el título del item."""

import sqlite3
from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/compras")
def mis_compras(usuario_id: str):
    conn = sqlite3.connect("compras.db")
    conn.row_factory = sqlite3.Row
    compras = conn.execute(
        "SELECT id, item_id, precio_centavos, comprada_en FROM compras WHERE usuario_id = ?",
        (usuario_id,),
    ).fetchall()
    out = []
    for c in compras:
        item = conn.execute(
            "SELECT titulo FROM items_cache WHERE id = ?", (c["item_id"],)
        ).fetchone()
        out.append({**dict(c), "item_titulo": item["titulo"] if item else None})
    return {"items": out}

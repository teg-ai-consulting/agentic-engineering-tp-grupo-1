"""vendedores-service — stub. Datos públicos del vendedor.

Expone la lectura individual y la BATCH (`?ids=`) — esta última es la que
tendría que usar items-service para el listado, en vez del N+1.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="vendedores-service")

_VENDEDORES = {
    "v1": {"id": "v1", "nombre": "TiendaTech", "reputacion": "verde"},
    "v2": {"id": "v2", "nombre": "HogarYMas", "reputacion": "verde"},
    "v3": {"id": "v3", "nombre": "ModaSur", "reputacion": "amarillo"},
}


@app.get("/v1/vendedores/{vendedor_id}")
def obtener(vendedor_id: str) -> dict:
    v = _VENDEDORES.get(vendedor_id)
    if v is None:
        raise HTTPException(status_code=404, detail="vendedor no encontrado")
    return v


@app.get("/v1/vendedores")
def batch(ids: str = Query(..., description="ids separados por coma")) -> dict:
    pedidos = [i for i in ids.split(",") if i]
    return {"vendedores": [_VENDEDORES[i] for i in pedidos if i in _VENDEDORES]}

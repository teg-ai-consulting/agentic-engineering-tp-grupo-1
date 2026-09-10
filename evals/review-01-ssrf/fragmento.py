"""PR de ejemplo: previsualizar la foto de perfil de un vendedor."""

import requests
from fastapi import APIRouter

router = APIRouter()


@router.post("/v1/vendedores/{vendedor_id}/foto-preview")
def preview(vendedor_id: str, body: dict):
    url = body["url"]
    r = requests.get(url, timeout=3)
    return {"content_type": r.headers.get("content-type"), "bytes": len(r.content)}

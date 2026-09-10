"""usuarios-service — stub. Auth (JWT) y perfil del comprador.

El login devuelve un JWT con `sub` = id del usuario. Los servicios de datos
personales (compras-service) sacan la identidad de ahí, nunca del request
(ADR-0005).
"""

from __future__ import annotations

import base64
import json

from fastapi import FastAPI, HTTPException

app = FastAPI(title="usuarios-service")

_USUARIOS = {
    "u1": {"id": "u1", "email": "ana@example.com", "nombre": "Ana"},
    "u2": {"id": "u2", "email": "beto@example.com", "nombre": "Beto"},
}


def _fake_jwt(sub: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"sub": sub}).encode()).decode()
    return f"fake.{payload}.sig"


@app.post("/v1/auth/login")
def login(body: dict) -> dict:
    for u in _USUARIOS.values():
        if u["email"] == body.get("email"):
            return {"access_token": _fake_jwt(u["id"]), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="credenciales inválidas")


@app.get("/v1/usuarios/{usuario_id}")
def obtener(usuario_id: str) -> dict:
    u = _USUARIOS.get(usuario_id)
    if u is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return u

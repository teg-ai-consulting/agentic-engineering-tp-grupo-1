"""REFERENCIA — el test de regresión que tu agente de QA tiene que producir en
la Parte 1. No lo copies tal cual: tu QA lo escribe (y lo pone en
`items-service/`, al lado de `test_items.py`).

Falla contra el código con el N+1. Pasa cuando se implemente el fix del ADR.

Para correrlo: `pytest incidente/regresion_referencia.py` desde
`marketplace/codigo-inicial/` (agrega items-service al path).
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "items-service"))

import main  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(main.app)


def test_listar_items_no_hace_n_mas_1():
    with main.query_counter() as count:
        r = client.get("/v1/items?limit=5")
    assert r.status_code == 200
    # 1 query por el listado + a lo sumo 1 batch por los vendedores. Nunca N+1.
    assert count() <= 2, f"el listado hizo {count()} queries — hay un N+1"

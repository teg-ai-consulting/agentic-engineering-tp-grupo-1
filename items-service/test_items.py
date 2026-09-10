"""CI baseline de items-service (happy path + error). Lo corre `ci.yml`."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_lista_items_ok():
    r = client.get("/v1/items?limit=3")
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 3
    assert body["items"][0]["vendedor_nombre"]  # resuelve el nombre del vendedor
    assert body["next_cursor"]


def test_item_no_encontrado():
    r = client.get("/v1/items/no-existe")
    assert r.status_code == 404

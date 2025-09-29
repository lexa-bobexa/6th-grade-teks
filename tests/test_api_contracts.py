from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_root_ok():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("ok") is True

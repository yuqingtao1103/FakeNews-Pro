from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_predict_minimal():
    r = client.post("/predict", json={"headline": "City council approves budget"})
    assert r.status_code == 200
    j = r.json()
    assert "label" in j and "proba" in j and "top_features" in j

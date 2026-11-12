from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_no_fabricated_offers():
    assert client.get("/api/v1/offers", params={"q": "amazon"}).json() == []

def test_invalid_category():
    assert client.get("/api/v1/offers", params={"category": "unknown"}).status_code == 422

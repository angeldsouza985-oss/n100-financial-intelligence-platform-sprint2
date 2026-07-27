from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_peers():
    response = client.get("/api/v1/peers/ABB")

    assert response.status_code == 200

    data = response.json()

    assert "sector" in data
    assert "companies" in data
    assert isinstance(data["companies"], list)
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_portfolio():
    response = client.get("/api/v1/portfolio/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_companies"] == 92
    assert "avg_roe" in data
    assert "avg_pe" in data
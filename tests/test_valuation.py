from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_valuation():
    response = client.get("/api/v1/valuation/ABB")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "ABB"
    assert "valuation_label" in data
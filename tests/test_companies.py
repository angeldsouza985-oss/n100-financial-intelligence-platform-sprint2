from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_companies():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_company():
    response = client.get("/api/v1/companies/ABB")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "ABB"


def test_get_company_ratios():
    response = client.get("/api/v1/companies/ABB/ratios")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
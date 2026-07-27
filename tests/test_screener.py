from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener():
    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_screener_filters():
    response = client.get(
        "/api/v1/screener?roe_min=20&de_max=1&fcf_min=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for company in data:
        assert company["return_on_equity_pct"] >= 20
        assert company["debt_to_equity"] <= 1
        assert company["free_cash_flow"] >= 0
from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_cfo_quality_high():
    assert cfo_quality_score(120, 100) == "High Quality"


def test_cfo_quality_moderate():
    assert cfo_quality_score(70, 100) == "Moderate"


def test_cfo_quality_accrual():
    assert cfo_quality_score(20, 100) == "Accrual Risk"


def test_capex_intensity():
    value, label = capex_intensity(-50, 1000)
    assert round(value, 2) == 5.00
    assert label == "Moderate"


def test_fcf_conversion():
    assert round(fcf_conversion_rate(300, 600), 2) == 50.00


def test_capital_allocation():
    signs, label = capital_allocation_pattern(100, -50, -20)
    assert signs == ("+", "-", "-")
    assert label == "Reinvestor"


def test_shareholder_returns():
    signs, label = capital_allocation_pattern(
        100,
        -50,
        -20,
        cfo_pat_ratio=1.2
    )
    assert label == "Shareholder Returns"
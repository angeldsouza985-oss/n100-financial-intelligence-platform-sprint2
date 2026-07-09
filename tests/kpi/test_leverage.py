from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover
)


def test_debt_free():
    assert debt_to_equity(0, 100, 200) == 0


def test_debt_to_equity():
    assert round(debt_to_equity(150, 100, 200), 2) == 0.50


def test_high_leverage():
    assert high_leverage_flag(6, "IT") is True


def test_financial_no_flag():
    assert high_leverage_flag(8, "Financials") is False


def test_interest_zero():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_net_debt():
    assert net_debt(300, 100) == 200


def test_asset_turnover():
    assert round(asset_turnover(1000, 500), 2) == 2.00
import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_difference
)


def test_net_profit_margin():
    assert round(net_profit_margin(100, 1000), 2) == 10.00


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert round(operating_profit_margin(150, 1000), 2) == 15.00


def test_opm_difference():
    assert check_opm_difference(15, 13) is True


def test_roe():
    assert round(return_on_equity(100, 200, 300), 2) == 20.00


def test_negative_equity():
    assert return_on_equity(100, -100, -50) is None


def test_roce():
    assert round(
        return_on_capital_employed(
            120,
            200,
            300,
            100
        ),
        2
    ) == 20.00


def test_roa():
    assert round(return_on_assets(100, 500), 2) == 20.00
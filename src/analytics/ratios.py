"""
Sprint 2 - Financial Ratios
"""


def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    if sales == 0:
        return None
    return (operating_profit / sales) * 100


def check_opm_difference(calculated, source):
    """
    Returns True if OPM difference exceeds 1%
    """
    if calculated is None or source is None:
        return False

    return abs(calculated - source) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
):
    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def return_on_assets(net_profit, total_assets):
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def debt_to_equity(
    borrowings,
    equity_capital,
    reserves,
):
    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(de_ratio, broad_sector):
    """
    Suppress leverage warning for Financials.
    """

    if de_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return de_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    if icr is None:
        return "Debt Free"

    return ""


def icr_warning_flag(icr):
    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments,
):
    return borrowings - investments


def asset_turnover(
    sales,
    total_assets,
):
    if total_assets == 0:
        return None

    return sales / total_assets
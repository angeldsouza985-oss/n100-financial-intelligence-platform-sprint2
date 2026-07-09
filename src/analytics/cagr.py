"""
Sprint 2 - Day 10
CAGR Engine
"""

from math import pow


def calculate_cagr(start_value, end_value, years):
    """
    CAGR = ((End / Start)^(1/Years) - 1) × 100
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (pow(end_value / start_value, 1 / years) - 1) * 100

    return cagr, None


def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


def pat_cagr(start_pat, end_pat, years):
    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)
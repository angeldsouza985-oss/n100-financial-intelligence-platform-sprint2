"""
Sprint 2 - Day 11
Cash Flow KPIs
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = Operating Activity + Investing Activity
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """
    CFO / PAT Quality Score
    """
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity = |Investing Activity| / Sales × 100
    """
    if sales == 0:
        return None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return intensity, label


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion = FCF / Operating Profit × 100
    """
    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Classify capital allocation pattern.
    """
    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    label = patterns.get(signs, "Unknown")

    if (
        signs == ("+", "-", "-")
        and cfo_pat_ratio is not None
        and cfo_pat_ratio > 1
    ):
        label = "Shareholder Returns"

    return signs, label
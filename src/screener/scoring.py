import pandas as pd


def normalize(series):
    """
    Normalize a metric to a 0–100 scale.
    """

    minimum = series.min()
    maximum = series.max()

    if minimum == maximum:
        return pd.Series(50, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


def inverse_normalize(series):
    """
    Lower values are better (e.g. Debt to Equity).
    """

    return 100 - normalize(series)


def compute_quality_score(df):

    df = df.copy()

    # ------------------------
    # Normalize KPIs
    # ------------------------

    df["roe_score"] = normalize(df["return_on_equity_pct"])

    df["roce_score"] = normalize(
        df["return_on_capital_employed_pct"]
    )

    df["npm_score"] = normalize(
        df["net_profit_margin_pct"]
    )

    df["revenue_growth_score"] = normalize(
        df["revenue_cagr_5yr"]
    )

    df["pat_growth_score"] = normalize(
        df["pat_cagr_5yr"]
    )

    df["fcf_score"] = normalize(
        df["free_cash_flow"]
    )

    df["fcf_conversion_score"] = normalize(
        df["fcf_conversion_rate"]
    )

    df["de_score"] = inverse_normalize(
        df["debt_to_equity"]
    )

    df["interest_score"] = normalize(
        df["interest_coverage"]
    )

    # ------------------------
    # Composite Score
    # ------------------------

    df["composite_quality_score"] = (

        df["roe_score"] * 0.15 +

        df["roce_score"] * 0.10 +

        df["npm_score"] * 0.10 +

        df["fcf_score"] * 0.15 +

        df["fcf_conversion_score"] * 0.10 +

        df["revenue_growth_score"] * 0.10 +

        df["pat_growth_score"] * 0.10 +

        df["de_score"] * 0.10 +

        df["interest_score"] * 0.10

    )

    return df
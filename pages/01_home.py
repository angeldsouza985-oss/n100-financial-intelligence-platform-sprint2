import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_ratios,
    get_sectors,
)

st.title("🏠 Home Dashboard")

# -----------------------------
# Sidebar
# -----------------------------
year = st.sidebar.selectbox(
    "Select Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5,
)

# -----------------------------
# Load Data
# -----------------------------
try:
    df = get_ratios(year)
except Exception as e:
    st.error(f"Unable to load financial ratios.\n\n{e}")
    st.stop()

if df.empty:
    st.warning("No data found for the selected year.")
    st.stop()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

avg_roe = df["return_on_equity_pct"].mean()
median_pe = df["pe_ratio"].median()
median_de = df["debt_to_equity"].median()
total_companies = df["company_id"].nunique()
median_rev_cagr = df["revenue_cagr_5yr"].median()
debt_free = (df["debt_to_equity"] == 0).sum()

col1.metric("Average ROE", f"{avg_roe:.2f}%")
col2.metric("Median P/E", f"{median_pe:.2f}")
col3.metric("Median D/E", f"{median_de:.2f}")

col4.metric("Companies", total_companies)
col5.metric("Median Revenue CAGR", f"{median_rev_cagr:.2f}%")
col6.metric("Debt-Free Companies", debt_free)

st.divider()

# -----------------------------
# Sector Distribution
# -----------------------------
try:
    sector_df = get_sectors()

    sector_count = (
        sector_df.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_count,
        names="broad_sector",
        values="Companies",
        hole=0.45,
        title="Sector Distribution",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

except Exception as e:
    st.error(f"Sector chart error:\n\n{e}")

st.divider()

# -----------------------------
# Top 5 Companies
# -----------------------------
st.subheader("🏆 Top 5 Companies by Quality Score")

try:
    top = df.copy()

    top["quality_score"] = (
        top["return_on_equity_pct"]
        + top["return_on_capital_employed_pct"]
        + top["net_profit_margin_pct"]
    )

    top = (
        top.sort_values(
            "quality_score",
            ascending=False,
        )[["company_id", "quality_score"]]
        .head(5)
    )

    st.dataframe(
        top,
        use_container_width=True,
    )

except Exception as e:
    st.error(f"Unable to generate Top 5 table.\n\n{e}")
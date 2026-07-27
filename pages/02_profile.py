import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_company_trend,
    get_sectors,
)

st.title("🏢 Company Profile")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"],
)

df = get_company_trend(company)

if df.empty:
    st.warning("Ticker not found — please try another.")
    st.stop()

sector_df = get_sectors()

sector = sector_df[
    sector_df["company_id"] == company
]

# ----------------------------
# Company Information
# ----------------------------

st.subheader(company)

if not sector.empty:
    c1, c2 = st.columns(2)

    c1.write(f"**Sector:** {sector.iloc[0]['broad_sector']}")
    c2.write(f"**Sub-sector:** {sector.iloc[0]['sub_sector']}")

st.divider()

# ----------------------------
# KPI Cards
# ----------------------------

latest = df.iloc[-1]

k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

k1.metric(
    "ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

k2.metric(
    "ROCE",
    f"{latest['return_on_capital_employed_pct']:.2f}%"
)

k3.metric(
    "Net Profit Margin",
    f"{latest['net_profit_margin_pct']:.2f}%"
)

k4.metric(
    "Debt / Equity",
    f"{latest['debt_to_equity']:.2f}"
)

k5.metric(
    "Revenue CAGR",
    f"{latest['revenue_cagr_5yr']:.2f}%"
)

k6.metric(
    "Free Cash Flow",
    f"{latest['free_cash_flow']:.0f}"
)

st.divider()

# ----------------------------
# Revenue & Net Profit
# ----------------------------

chart1 = px.bar(
    df,
    x="merge_year",
    y=["sales", "net_profit"],
    barmode="group",
    title="Revenue & Net Profit",
)

st.plotly_chart(
    chart1,
    use_container_width=True,
)

# ----------------------------
# ROE & ROCE
# ----------------------------

chart2 = px.line(
    df,
    x="merge_year",
    y=[
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
    ],
    markers=True,
    title="ROE vs ROCE",
)

st.plotly_chart(
    chart2,
    use_container_width=True,
)

# ----------------------------
# Pros & Cons
# ----------------------------

st.subheader("Pros")

pros = []

if latest["return_on_equity_pct"] >= 15:
    pros.append("✅ Strong ROE")

if latest["debt_to_equity"] <= 1:
    pros.append("✅ Low Debt")

if latest["revenue_cagr_5yr"] >= 10:
    pros.append("✅ Good Revenue Growth")

if len(pros) == 0:
    pros.append("No major strengths identified.")

for p in pros:
    st.write(p)

st.subheader("Cons")

cons = []

if latest["pe_ratio"] > 40:
    cons.append("❌ High P/E")

if latest["debt_to_equity"] > 2:
    cons.append("❌ High Debt")

if latest["free_cash_flow"] < 0:
    cons.append("❌ Negative Free Cash Flow")

if len(cons) == 0:
    cons.append("No major concerns identified.")

for c in cons:
    st.write(c)
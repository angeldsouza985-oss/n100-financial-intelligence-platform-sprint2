import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_ratios

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("🔎 Stock Screener")

# ==============================
# Sidebar
# ==============================

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5,
)

df = get_ratios(year)

if df.empty:
    st.warning("No data available.")
    st.stop()

# ==============================
# Quick Presets
# ==============================

st.sidebar.subheader("Quick Presets")

preset = st.sidebar.radio(
    "Choose a preset",
    [
        "Custom",
        "Quality",
        "Value",
        "Growth",
        "Dividend",
        "Debt-Free",
        "Turnaround",
    ]
)

# Default values
roe_default = 15.0
de_default = 2.0
pe_default = 30.0
pb_default = 5.0
opm_default = 10.0
rev_default = 5.0
pat_default = 5.0
div_default = 1.0
icr_default = 3.0
fcf_default = -100000.0

if preset == "Quality":
    roe_default = 20
    de_default = 1
    opm_default = 20

elif preset == "Value":
    pe_default = 20
    pb_default = 3

elif preset == "Growth":
    rev_default = 15
    pat_default = 15

elif preset == "Dividend":
    div_default = 3

elif preset == "Debt-Free":
    de_default = 0.2

elif preset == "Turnaround":
    rev_default = 0
    pat_default = 0

# ==============================
# Sliders
# ==============================

roe = st.sidebar.slider("Minimum ROE (%)", 0.0, 100.0, float(roe_default))

de = st.sidebar.slider("Maximum Debt/Equity", 0.0, 20.0, float(de_default))

pe = st.sidebar.slider("Maximum P/E", 0.0, 150.0, float(pe_default))

pb = st.sidebar.slider("Maximum P/B", 0.0, 20.0, float(pb_default))

opm = st.sidebar.slider("Minimum OPM (%)", 0.0, 100.0, float(opm_default))

rev = st.sidebar.slider("Minimum Revenue CAGR (%)", -20.0, 50.0, float(rev_default))

pat = st.sidebar.slider("Minimum PAT CAGR (%)", -20.0, 50.0, float(pat_default))

dividend = st.sidebar.slider("Minimum Dividend Yield (%)", 0.0, 10.0, float(div_default))

interest = st.sidebar.slider("Minimum Interest Coverage", 0.0, 100.0, float(icr_default))

fcf = st.sidebar.slider("Minimum Free Cash Flow", -100000.0, 100000.0, float(fcf_default))

# ==============================
# Filtering
# ==============================

filtered = df.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"] >= roe)
    & (filtered["debt_to_equity"] <= de)
    & (filtered["pe_ratio"] <= pe)
    & (filtered["pb_ratio"] <= pb)
    & (filtered["operating_profit_margin_pct"] >= opm)
    & (filtered["revenue_cagr_5yr"] >= rev)
    & (filtered["pat_cagr_5yr"] >= pat)
    & (filtered["dividend_yield_pct"] >= dividend)
    & (filtered["interest_coverage"] >= interest)
    & (filtered["free_cash_flow"] >= fcf)
]

# ==============================
# KPI Cards
# ==============================

c1, c2, c3 = st.columns(3)

c1.metric("Companies Found", len(filtered))

if len(filtered) > 0:
    c2.metric(
        "Average ROE",
        f"{filtered['return_on_equity_pct'].mean():.2f}%"
    )

    c3.metric(
        "Average P/E",
        f"{filtered['pe_ratio'].mean():.2f}"
    )
else:
    c2.metric("Average ROE", "0")
    c3.metric("Average P/E", "0")

st.divider()

# ==============================
# Results Table
# ==============================

st.subheader("Matching Companies")

display = filtered[
    [
        "company_id",
        "return_on_equity_pct",
        "pe_ratio",
        "pb_ratio",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "dividend_yield_pct",
        "interest_coverage",
        "free_cash_flow",
    ]
].copy()

display.columns = [
    "Company",
    "ROE %",
    "P/E",
    "P/B",
    "Debt/Equity",
    "OPM %",
    "Revenue CAGR %",
    "PAT CAGR %",
    "Dividend %",
    "Interest Coverage",
    "Free Cash Flow",
]

display = display.round(2)

display = display.sort_values(
    by="ROE %",
    ascending=False,
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

# ==============================
# Download CSV
# ==============================

csv = display.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    csv,
    "screener_results.csv",
    "text/csv",
)

st.success(f"✅ {len(display)} companies match your filters.")
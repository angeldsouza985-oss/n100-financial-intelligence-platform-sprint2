import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_ratios

st.title("🔍 Stock Screener")

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5,
)

df = get_ratios(year)

# -----------------------------
# Sliders
# -----------------------------

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0.0,
    100.0,
    15.0,
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0,
)

pe = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    100.0,
    30.0,
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"] >= roe
]

filtered = filtered[
    filtered["debt_to_equity"] <= de
]

filtered = filtered[
    filtered["pe_ratio"] <= pe
]

st.subheader(f"Matching Companies: {len(filtered)}")

st.dataframe(
    filtered,
    use_container_width=True,
)

# -----------------------------
# CSV Download
# -----------------------------

csv = filtered.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv",
)
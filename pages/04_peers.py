import streamlit as st
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_peer_groups,
    get_peer_companies,
)

st.title("📊 Peer Comparison")

groups = get_peer_groups()

selected_group = st.selectbox(
    "Select Peer Group",
    groups["peer_group_name"]
)

df = get_peer_companies(selected_group)

if df.empty:
    st.warning("No companies found.")
    st.stop()

company = st.selectbox(
    "Select Company",
    df["company_id"]
)
st.divider()

# -----------------------------
# Radar Chart
# -----------------------------

selected = df[df["company_id"] == company].iloc[0]

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "revenue_cagr_5yr",
]

labels = [
    "ROE",
    "ROCE",
    "Net Margin",
    "OPM",
    "Revenue CAGR",
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=[selected[m] for m in metrics],
        theta=labels,
        fill="toself",
        name=company,
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=500,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Peer Comparison")

display = df[
    [
        "company_id",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "pe_ratio",
        "pb_ratio",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "is_benchmark",
    ]
].copy()

display.columns = [
    "Company",
    "ROE %",
    "ROCE %",
    "Net Margin %",
    "P/E",
    "P/B",
    "Debt/Equity",
    "OPM %",
    "Revenue CAGR %",
    "Benchmark",
]

display = display.round(2)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)
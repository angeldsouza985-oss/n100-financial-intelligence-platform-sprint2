import sqlite3
import streamlit as st
import plotly.express as px

import src.dashboard.utils.db as db


st.title("📈 Trend Analysis")

companies = db.get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"],
)

df = db.get_company_trend(company)

if df.empty:
    st.warning("No data found.")
    st.stop()

metrics = {
    "Sales": "sales",
    "Net Profit": "net_profit",
    "Operating Profit": "operating_profit",
    "ROE": "return_on_equity_pct",
    "ROCE": "return_on_capital_employed_pct",
    "P/E": "pe_ratio",
    "P/B": "pb_ratio",
    "Free Cash Flow": "free_cash_flow",
    "Revenue CAGR": "revenue_cagr_5yr",
}

selected = st.multiselect(
    "Choose up to 3 metrics",
    list(metrics.keys()),
    default=["Sales"],
    max_selections=3,
)

if len(selected) == 0:
    st.info("Select at least one metric.")
    st.stop()

plot_df = df[["merge_year"]].copy()

for item in selected:
    plot_df[item] = df[metrics[item]]

plot_df = plot_df.melt(
    id_vars="merge_year",
    var_name="Metric",
    value_name="Value",
)

fig = px.line(
    plot_df,
    x="merge_year",
    y="Value",
    color="Metric",
    markers=True,
    title=f"{company} Trend Analysis",
)

fig.update_layout(
    height=600,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)
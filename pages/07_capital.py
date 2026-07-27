import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("💰 Capital Allocation")

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT
    company_id,
    market_cap_crore,
    enterprise_value_crore,
    pe_ratio,
    pb_ratio,
    dividend_yield_pct
FROM market_cap
WHERE year = 2024
""", conn)

conn.close()

if df.empty:
    st.warning("No market cap data found.")
    st.stop()

# ----------------------------
# KPI Cards
# ----------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(df)
)

c2.metric(
    "Total Market Cap",
    f"{df['market_cap_crore'].sum():,.0f} Cr"
)

c3.metric(
    "Average Dividend Yield",
    f"{df['dividend_yield_pct'].mean():.2f}%"
)

st.divider()

# ----------------------------
# Company Selector
# ----------------------------

company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

company_df = df[df["company_id"] == company]

st.subheader(f"{company} Capital Metrics")

st.dataframe(
    company_df.round(2),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ----------------------------
# Bubble Chart
# ----------------------------

fig = px.scatter(
    df,
    x="pe_ratio",
    y="pb_ratio",
    size="market_cap_crore",
    color="company_id",
    hover_name="company_id",
    title="Market Capitalization Analysis",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

# ----------------------------
# Top 10 Companies
# ----------------------------

st.subheader("Top 10 Companies by Market Cap")

top10 = (
    df.sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(10)
)

fig2 = px.bar(
    top10,
    x="company_id",
    y="market_cap_crore",
    color="market_cap_crore",
    title="Top 10 Market Cap Companies",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

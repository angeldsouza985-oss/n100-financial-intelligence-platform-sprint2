import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("🫧 Sector Analysis")

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT
    s.broad_sector,
    s.company_id,
    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.market_cap_crore,
    fr.pe_ratio,
    fr.pb_ratio,
    fr.debt_to_equity
FROM sectors s
JOIN financial_ratios fr
ON s.company_id = fr.company_id
WHERE fr.merge_year = 2024
""", conn)

conn.close()

if df.empty:
    st.warning("No data found.")
    st.stop()

sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].unique())
)

sector_df = df[df["broad_sector"] == sector]

# KPI Cards
c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(sector_df)
)

c2.metric(
    "Average ROE",
    f"{sector_df['return_on_equity_pct'].mean():.2f}%"
)

c3.metric(
    "Average P/E",
    f"{sector_df['pe_ratio'].mean():.2f}"
)

st.divider()

fig = px.scatter(
    sector_df,
    x="return_on_equity_pct",
    y="pe_ratio",
    size="market_cap_crore",
    color="company_id",
    hover_name="company_id",
    title=f"{sector} Companies",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

display = sector_df[[
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "debt_to_equity",
]]

display.columns = [
    "Company",
    "ROE %",
    "ROCE %",
    "Net Margin %",
    "Market Cap",
    "P/E",
    "P/B",
    "Debt/Equity",
]

st.dataframe(
    display.round(2),
    use_container_width=True,
    hide_index=True,
)
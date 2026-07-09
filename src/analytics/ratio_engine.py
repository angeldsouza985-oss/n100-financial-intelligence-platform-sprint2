
import os
import sys
import sqlite3
import pandas as pd

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    print("Current file:", __file__)
print("Project root:", PROJECT_ROOT)
print("Exists:", os.path.exists(PROJECT_ROOT))
print("Contents:", os.listdir(PROJECT_ROOT))

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)


print("Connecting to database...")

conn = sqlite3.connect("nifty100.db")

print("Loading tables...")

pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

print("Merging tables...")

df = (
    pnl.merge(bs, on=["company_id", "year"])
       .merge(cf, on=["company_id", "year"])
)

print("Calculating KPIs...")

df["net_profit_margin_pct"] = df.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"],
    ),
    axis=1,
)

df["operating_profit_margin_pct"] = df.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"],
    ),
    axis=1,
)

df["return_on_equity_pct"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"],
    ),
    axis=1,
)

df["return_on_capital_employed_pct"] = df.apply(
    lambda x: return_on_capital_employed(
        x["operating_profit"],
        x["equity_capital"],
        x["reserves"],
        x["borrowings"],
    ),
    axis=1,
)

df["return_on_assets_pct"] = df.apply(
    lambda x: return_on_assets(
        x["net_profit"],
        x["total_assets"],
    ),
    axis=1,
)

df["debt_to_equity"] = df.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"],
    ),
    axis=1,
)

df["interest_coverage"] = df.apply(
    lambda x: interest_coverage_ratio(
        x["operating_profit"],
        x["other_income"],
        x["interest"],
    ),
    axis=1,
)

df["asset_turnover"] = df.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["total_assets"],
    ),
    axis=1,
)
print("\nColumns in DataFrame:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df[["company_id", "year"]].head())

# --------------------------------------------
# Clean DataFrame before saving
# --------------------------------------------

# Remove duplicate id columns created during merge
drop_cols = [col for col in ["id_x", "id_y", "id"] if col in df.columns]

if drop_cols:
    df = df.drop(columns=drop_cols)

# Preserve company_id
df["company_id"] = df["company_id"].astype(str)

# Move company_id to the first column
cols = ["company_id"] + [c for c in df.columns if c != "company_id"]
df = df[cols]

print("\nFinal Columns:")
print(df.columns.tolist())

print("\nSaving financial_ratios table...")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False,
)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
rows = cursor.fetchone()[0]

print(f"\nRows inserted: {rows}")

print("\nFinancial Ratios Table Schema:")
cursor.execute("PRAGMA table_info(financial_ratios)")
for column in cursor.fetchall():
    print(column)

conn.close()

print("\nSprint 2 Day 12 Completed.")
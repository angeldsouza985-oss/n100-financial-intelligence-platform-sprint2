
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
from src.analytics.cashflow_kpis import (
    free_cash_flow,
    fcf_conversion_rate,
)
from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


print("Connecting to database...")

conn = sqlite3.connect("nifty100.db")

print("Loading tables...")


pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)
market = pd.read_sql("SELECT * FROM market_cap", conn)
# Convert financial statement year ("Mar 2024") -> 2024
# Extract 4-digit year
pnl["merge_year"] = pnl["year"].astype(str).str.extract(r"(\d{4})")

# Show rows where extraction failed
print("\nRows with invalid year:")
print(pnl[pnl["merge_year"].isna()][["company_id", "year"]].head(20))

# Drop invalid rows for now
pnl = pnl.dropna(subset=["merge_year"])

# Convert to integer
pnl["merge_year"] = pnl["merge_year"].astype(int)

# market_cap already stores year as INTEGER
market["merge_year"] = market["year"]

print("Merging tables...")


df = (
    pnl.merge(bs, on=["company_id", "year"])
       .merge(cf, on=["company_id", "year"])
)

df = df.merge(
    market[
        [
            "company_id",
            "merge_year",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
        ]
    ],
    on=["company_id", "merge_year"],
    how="left",
)
# Keep only financial years
df = df[df["merge_year"].notna()].copy()

# Remove duplicate company-year records
df = df.sort_values(["company_id", "merge_year"])
df = df.drop_duplicates(
    subset=["company_id", "merge_year"],
    keep="last",
)
def calculate_company_cagr(df, company_id):
    company = df[df["company_id"] == company_id].copy()

    company = company.sort_values("merge_year")

    latest = company.iloc[-1]

    five_years = company[
        company["merge_year"] <= latest["merge_year"] - 5
    ]

    if five_years.empty:
        return None, None, None

    start = five_years.iloc[-1]

    rev, _ = revenue_cagr(
        start["sales"],
        latest["sales"],
        5,
    )

    pat, _ = pat_cagr(
        start["net_profit"],
        latest["net_profit"],
        5,
    )

    eps, _ = eps_cagr(
        start["eps"],
        latest["eps"],
        5,
    )

    return rev, pat, eps

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
# -----------------------------
# Cash Flow KPIs
# -----------------------------

df["free_cash_flow"] = df.apply(
    lambda x: free_cash_flow(
        x["operating_activity"],
        x["investing_activity"],
    ),
    axis=1,
)

df["fcf_conversion_rate"] = df.apply(
    lambda x: fcf_conversion_rate(
        x["free_cash_flow"],
        x["operating_profit"],
    ),
    axis=1,
)
cagr_rows = []

for company in df["company_id"].unique():

    rev, pat, eps = calculate_company_cagr(df, company)

    cagr_rows.append(
        {
            "company_id": company,
            "revenue_cagr_5yr": rev,
            "pat_cagr_5yr": pat,
            "eps_cagr_5yr": eps,
        }
    )

cagr_df = pd.DataFrame(cagr_rows)

df = df.merge(
    cagr_df,
    on="company_id",
    how="left",
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
print("\nCash Flow KPIs:")
print(
    df[
        [
            "company_id",
            "free_cash_flow",
            "fcf_conversion_rate",
        ]
    ].head()
)
print("\nCAGR KPIs:")

print(
    df[
        [
            "company_id",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
        ]
    ].head()
)

print("\nFinal Columns:")
print(df.columns.tolist())

print("\nSaving financial_ratios table...")
print("\nNew Market Columns:")
print("\nUnique Company-Year Records:")
print(df[["company_id", "merge_year"]].head(10))

print(
    df[
        [
            "company_id",
            "merge_year",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
        ]
    ].head()
)

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
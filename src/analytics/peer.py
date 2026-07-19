import os
import sys
import sqlite3
import pandas as pd

def percentile_rank(series, ascending=True):
    """
    Calculate percentile rank (0-100).
    Higher value = higher percentile unless ascending=False.
    """
    if ascending:
        return series.rank(pct=True) * 100
    else:
        return (1 - series.rank(pct=True)) * 100

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("Connecting to database...")

conn = sqlite3.connect("nifty100.db")

print("Loading tables...")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peers = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

print("Financial Ratios:", len(ratios))
print("Peer Groups:", len(peers))
print("\nMerging peer groups...")

df = ratios.merge(
    peers,
    on="company_id",
    how="left"
)

# Fill missing peer groups
df["peer_group_name"] = df["peer_group_name"].fillna(
    "No peer group assigned"
)

df["is_benchmark"] = df["is_benchmark"].fillna(0)

print("\nPeer Group Summary:")
print(df["peer_group_name"].value_counts())

print("\nSample Data:")
print(
    df[
        [
            "company_id",
            "peer_group_name",
            "is_benchmark",
        ]
    ].head(15)
)
print("\nCalculating percentile rankings...")

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "free_cash_flow",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover",
]

# Ignore companies without peer groups
peer_df = df[df["peer_group_name"] != "No peer group assigned"].copy()

# Higher is better
for metric in metrics:
    peer_df[f"{metric}_percentile"] = (
        peer_df.groupby("peer_group_name")[metric]
        .transform(percentile_rank)
    )

# Debt-to-Equity (lower is better)
peer_df["debt_to_equity_percentile"] = (
    peer_df.groupby("peer_group_name")["debt_to_equity"]
    .transform(lambda s: percentile_rank(s, ascending=False))
)

print("\nSample Percentile Rankings:")

print(
    peer_df[
        [
            "company_id",
            "peer_group_name",
            "return_on_equity_pct",
            "return_on_equity_pct_percentile",
            "debt_to_equity",
            "debt_to_equity_percentile",
        ]
    ].head(15)
)
print("\nSaving peer_percentiles table...")

percentile_cols = [
    "company_id",
    "peer_group_name",
    "return_on_equity_pct_percentile",
    "return_on_capital_employed_pct_percentile",
    "net_profit_margin_pct_percentile",
    "free_cash_flow_percentile",
    "revenue_cagr_5yr_percentile",
    "pat_cagr_5yr_percentile",
    "eps_cagr_5yr_percentile",
    "interest_coverage_percentile",
    "asset_turnover_percentile",
    "debt_to_equity_percentile",
]

peer_df[percentile_cols].to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False,
)

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM peer_percentiles"
)

print(
    "Rows inserted:",
    cursor.fetchone()[0]
)
from openpyxl import Workbook
import os

print("\nGenerating peer_comparison.xlsx...")

wb = Workbook()
wb.remove(wb.active)

for group in sorted(peer_df["peer_group_name"].unique()):

    sheet = wb.create_sheet(title=group[:31])

    group_df = peer_df[
        peer_df["peer_group_name"] == group
    ].copy()

    sheet.append(list(group_df.columns))

    for row in group_df.itertuples(index=False):
        sheet.append(list(row))

os.makedirs("output", exist_ok=True)

wb.save("output/peer_comparison.xlsx")

print("peer_comparison.xlsx generated successfully!")
conn.close()

print("\npeer_percentiles table created successfully!")
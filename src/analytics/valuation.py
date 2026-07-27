import os
import sqlite3
import pandas as pd

DB = "nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB)

# Load data
ratios = pd.read_sql("""
SELECT
    company_id,
    merge_year,
    free_cash_flow
FROM financial_ratios
WHERE merge_year = (
    SELECT MAX(merge_year)
    FROM financial_ratios
)
""", conn)

market = pd.read_sql("""
SELECT
    company_id,
    market_cap_crore,
    pe_ratio,
    pb_ratio,
    ev_ebitda
FROM market_cap
WHERE year = (
    SELECT MAX(year)
    FROM market_cap
)
""", conn)

sector = pd.read_sql("""
SELECT
    company_id,
    broad_sector
FROM sectors
""", conn)

conn.close()

# Merge
df = (
    ratios
    .merge(market, on="company_id", how="left")
    .merge(sector, on="company_id", how="left")
)

# -------------------------
# FCF Yield
# -------------------------

df["fcf_yield_pct"] = (
    df["free_cash_flow"] /
    df["market_cap_crore"]
) * 100

# -------------------------
# Sector Median PE
# -------------------------

sector_median = (
    df.groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
    .rename(columns={"pe_ratio": "sector_median_pe"})
)

df = df.merge(
    sector_median,
    on="broad_sector",
    how="left"
)

# -------------------------
# PE vs Sector Median
# -------------------------

df["pe_vs_sector_median_pct"] = (
    df["pe_ratio"] /
    df["sector_median_pe"]
) * 100

# -------------------------
# Flags
# -------------------------

def valuation_flag(row):

    if pd.isna(row["pe_ratio"]) or pd.isna(row["sector_median_pe"]):
        return "N/A"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"

df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

# -------------------------
# Final Output
# -------------------------

summary = df[
    [
        "company_id",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag",
    ]
].copy()

summary.rename(
    columns={
        "broad_sector": "sector",
        "sector_median_pe": "sector_median_pe",
    },
    inplace=True,
)

summary.to_excel(
    os.path.join(
        OUTPUT_DIR,
        "valuation_summary.xlsx"
    ),
    index=False,
)

summary[
    summary["flag"].isin(
        ["Caution", "Discount"]
    )
].to_csv(
    os.path.join(
        OUTPUT_DIR,
        "valuation_flags.csv"
    ),
    index=False,
)

print("=" * 50)
print("Valuation completed successfully")
print(f"Companies processed : {len(summary)}")
print(f"Caution/Discount    : {len(summary[summary['flag'].isin(['Caution','Discount'])])}")
print("=" * 50)
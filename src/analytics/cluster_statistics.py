import os
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import zscore

DB = "nifty100.db"

OUTPUT = "output"
REPORTS = "reports"

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT
    s.company_id,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.return_on_assets_pct,
    fr.debt_to_equity,
    fr.pe_ratio,
    fr.pb_ratio,
    fr.operating_profit_margin_pct,
    fr.net_profit_margin_pct,
    fr.revenue_cagr_5yr,
    fr.free_cash_flow

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.merge_year = 2024
""", conn)

conn.close()

df["broad_sector"] = df["broad_sector"].fillna("Unknown")

kpis = [

    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "return_on_assets_pct",
    "debt_to_equity",
    "pe_ratio",
    "pb_ratio",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "free_cash_flow",

]

# ===================================
# Correlation Heatmap
# ===================================

corr = df[kpis].corr(method="pearson")

plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
)

plt.title("KPI Correlation Matrix")

plt.tight_layout()

plt.savefig(
    "reports/correlation_heatmap.png",
    dpi=200,
)

plt.close()

# ===================================
# Outlier Detection
# ===================================

outliers = []

for sector, grp in df.groupby("broad_sector"):

    temp = grp.copy()

    for col in kpis:

        if temp[col].nunique() > 1:

            temp[col + "_z"] = zscore(
                temp[col],
                nan_policy="omit"
            )

    for _, row in temp.iterrows():

        for col in kpis:

            z_col = col + "_z"

            if z_col in temp.columns:

                value = row[z_col]

                if pd.notna(value):

                    if abs(value) > 3:

                        outliers.append({

                            "company_id": row["company_id"],

                            "sector": sector,

                            "metric": col,

                            "value": row[col],

                            "z_score": round(value,2),

                        })

outlier_df = pd.DataFrame(outliers)

outlier_df.to_csv(
    "output/outlier_report.csv",
    index=False,
)

# ===================================
# Portfolio Statistics
# ===================================

stats = []

for col in kpis:

    stats.append({

        "metric": col,

        "P10": df[col].quantile(0.10),

        "P25": df[col].quantile(0.25),

        "P50": df[col].median(),

        "P75": df[col].quantile(0.75),

        "P90": df[col].quantile(0.90),

        "Mean": df[col].mean(),

        "Std": df[col].std(),

    })

stats_df = pd.DataFrame(stats)

stats_df.to_csv(
    "output/portfolio_stats.csv",
    index=False,
)

print("=" * 50)
print("Cluster Statistics Complete")
print("Companies :", len(df))
print("Outliers  :", len(outlier_df))
print("KPIs      :", len(stats_df))
print("=" * 50)
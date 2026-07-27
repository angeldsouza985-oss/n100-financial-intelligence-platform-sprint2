import os
import sqlite3
import pandas as pd
import numpy as np

DB = "nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT *
FROM financial_ratios
ORDER BY company_id, merge_year
""", conn)

sector_df = pd.read_sql("""
SELECT company_id, broad_sector
FROM sectors
""", conn)

conn.close()

# Merge sector information
df = df.merge(sector_df, on="company_id", how="left")

results = []
distress = []

for company, grp in df.groupby("company_id"):

    grp = grp.sort_values("merge_year")

    latest = grp.iloc[-1]

    # -------------------------
    # CFO Quality
    # -------------------------

    valid = grp[grp["net_profit"] != 0]

    if len(valid) > 0:
        cfo_ratio = (
            valid["operating_activity"] /
            valid["net_profit"]
        ).mean()
    else:
        cfo_ratio = np.nan

    if pd.isna(cfo_ratio):
        quality = "Unknown"
    elif cfo_ratio > 1:
        quality = "High Quality"
    elif cfo_ratio >= 0.5:
        quality = "Moderate"
    else:
        quality = "Accrual Risk"

    # -------------------------
    # CapEx Intensity
    # -------------------------

    if latest["sales"] != 0:
        capex = (
            abs(latest["investing_activity"]) /
            latest["sales"]
        ) * 100
    else:
        capex = np.nan

    if pd.isna(capex):
        capex_label = "Unknown"
    elif capex < 3:
        capex_label = "Asset Light"
    elif capex <= 8:
        capex_label = "Moderate"
    else:
        capex_label = "Capital Intensive"

    # -------------------------
    # Distress Flag
    # -------------------------

    distress_flag = (
        latest["operating_activity"] < 0
        and latest["financing_activity"] > 0
    )

    if distress_flag:
        distress.append({
            "company_id": company,
            "operating_activity": latest["operating_activity"],
            "financing_activity": latest["financing_activity"],
            "net_profit": latest["net_profit"]
        })

    # -------------------------
    # Deleveraging Flag
    # -------------------------

    if len(grp) >= 2:
        prev = grp.iloc[-2]

        deleveraging = (
            latest["financing_activity"] < 0
            and latest["borrowings"] < prev["borrowings"]
        )
    else:
        deleveraging = False

    # -------------------------
    # Capital Allocation Label
    # -------------------------

    if distress_flag:
        capital = "Distress Signal"

    elif latest["free_cash_flow"] > 0 and capex > 8:
        capital = "Reinvestor"

    elif latest["free_cash_flow"] > 0:
        capital = "Cash Generator"

    else:
        capital = "Neutral"

    results.append({

        "company_id": company,
        "sector": latest["broad_sector"],

        "cfo_quality_score": round(cfo_ratio, 2)
        if not pd.isna(cfo_ratio) else None,

        "cfo_quality_label": quality,

        "capex_intensity_pct": round(capex, 2)
        if not pd.isna(capex) else None,

        "capex_label": capex_label,

        "fcf_cagr_5yr": latest["free_cash_flow"],

        "fcf_conversion_pct": latest["fcf_conversion_rate"],

        "distress_flag": distress_flag,

        "deleveraging_flag": deleveraging,

        "capital_allocation_label": capital,

    })

cashflow = pd.DataFrame(results)

cashflow.to_excel(
    os.path.join(
        OUTPUT_DIR,
        "cashflow_intelligence.xlsx"
    ),
    index=False,
)

pd.DataFrame(distress).to_csv(
    os.path.join(
        OUTPUT_DIR,
        "distress_alerts.csv"
    ),
    index=False,
)

print("=" * 50)
print("Cash Flow Intelligence Complete")
print(f"Companies Processed : {len(cashflow)}")
print(f"Distress Alerts     : {len(distress)}")
print("=" * 50)
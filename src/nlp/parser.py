import os
import re
import sqlite3
import pandas as pd

INPUT_FILE = r"..\data\raw\analysis.xlsx"
DB = "nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read Excel (actual headers are on row 2)
df = pd.read_excel(INPUT_FILE, header=1)

pattern = re.compile(r"(\d+)\s*Years?:?\s*([\-\d.]+)%")

parsed_rows = []
failed_rows = []

fields = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in df.iterrows():

    company = row["company_id"]

    for field in fields:

        text = str(row[field])

        match = pattern.search(text)

        if match:

            parsed_rows.append({
                "company_id": company,
                "metric_type": field,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })

        else:

            failed_rows.append({
                "company_id": company,
                "metric_type": field,
                "original_text": text
            })

parsed = pd.DataFrame(parsed_rows)
failures = pd.DataFrame(failed_rows)

# -----------------------------
# Cross-validation
# -----------------------------

conn = sqlite3.connect(DB)

ratios = pd.read_sql("""
SELECT
    company_id,
    revenue_cagr_5yr,
    pat_cagr_5yr,
    return_on_equity_pct
FROM financial_ratios
WHERE merge_year = (
    SELECT MAX(merge_year)
    FROM financial_ratios
)
""", conn)

conn.close()

comparison = parsed.merge(
    ratios,
    on="company_id",
    how="left"
)

comparison["divergence_pct"] = None

for idx, row in comparison.iterrows():

    if row["metric_type"] == "compounded_sales_growth":
        expected = row["revenue_cagr_5yr"]

    elif row["metric_type"] == "compounded_profit_growth":
        expected = row["pat_cagr_5yr"]

    elif row["metric_type"] == "roe":
        expected = row["return_on_equity_pct"]

    else:
        continue

    if pd.notna(expected):

        comparison.loc[idx, "divergence_pct"] = abs(
            row["value_pct"] - expected
        )

comparison["manual_review"] = (
    comparison["divergence_pct"] > 5
)

comparison.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "analysis_parsed.csv"
    ),
    index=False,
)

failures.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "parse_failures.csv"
    ),
    index=False,
)

print("=" * 50)
print("Analysis Parser Complete")
print(f"Rows Parsed     : {len(parsed)}")
print(f"Parse Failures  : {len(failures)}")
print(f"Manual Reviews  : {comparison['manual_review'].sum()}")
print("=" * 50)
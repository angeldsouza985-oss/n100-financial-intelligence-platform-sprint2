import os
import sqlite3
import pandas as pd

DB = "nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT *
FROM financial_ratios
WHERE merge_year = (
    SELECT MAX(merge_year)
    FROM financial_ratios
)
""", conn)

conn.close()

results = []


def add(company, typ, rule, text, confidence):
    results.append({
        "company_id": company,
        "type": typ,
        "rule_id": rule,
        "text": text,
        "confidence_pct": confidence
    })


for _, row in df.iterrows():

    company = row["company_id"]

    pro_count = 0
    con_count = 0

    # -------------------------
    # PRO RULES
    # -------------------------

    if row["return_on_equity_pct"] >= 20:
        add(company, "Pro", "P1",
            "Consistently high return on equity demonstrates strong capital efficiency.",
            90)
        pro_count += 1

    if row["free_cash_flow"] > 0:
        add(company, "Pro", "P2",
            "Positive free cash flow indicates healthy cash generation.",
            85)
        pro_count += 1

    if row["debt_to_equity"] == 0:
        add(company, "Pro", "P3",
            "Debt-free balance sheet provides financial flexibility.",
            95)
        pro_count += 1

    if row["revenue_cagr_5yr"] >= 15:
        add(company, "Pro", "P4",
            "Revenue CAGR above 15% reflects strong business momentum.",
            88)
        pro_count += 1

    if row["operating_profit_margin_pct"] >= 25:
        add(company, "Pro", "P5",
            "Strong operating margins indicate pricing power.",
            82)
        pro_count += 1

    if row["interest_coverage"] >= 10:
        add(company, "Pro", "P6",
            "High interest coverage indicates low financial stress.",
            80)
        pro_count += 1

    # -------------------------
    # CON RULES
    # -------------------------

    if row["debt_to_equity"] > 2:
        add(company, "Con", "C1",
            f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated.",
            90)
        con_count += 1

    if row["free_cash_flow"] < 0:
        add(company, "Con", "C2",
            "Negative free cash flow raises concerns over cash generation.",
            85)
        con_count += 1

    if row["net_profit"] < 0:
        add(company, "Con", "C3",
            "Company reported a net loss in the latest year.",
            95)
        con_count += 1

    if row["interest_coverage"] < 1.5:
        add(company, "Con", "C4",
            "Interest coverage below 1.5x increases financial risk.",
            90)
        con_count += 1

    if row["return_on_capital_employed_pct"] < 10:
        add(company, "Con", "C5",
            "ROCE below 10% indicates weak capital efficiency.",
            80)
        con_count += 1

    if row["revenue_cagr_5yr"] < 5:
        add(company, "Con", "C6",
            "Revenue CAGR below 5% suggests limited growth.",
            75)
        con_count += 1

    # -------------------------
    # Guarantee at least one Pro
    # -------------------------

    if pro_count == 0:
        add(company, "Pro", "P0",
            "Business maintains stable financial performance.",
            65)

    # -------------------------
    # Guarantee at least one Con
    # -------------------------

    if con_count == 0:
        add(company, "Con", "C0",
            "Valuation and market conditions should continue to be monitored.",
            65)


output = pd.DataFrame(results)

output = output[
    output["confidence_pct"] >= 60
]

output.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "pros_cons_generated.csv"
    ),
    index=False,
)

print("=" * 50)
print("Pros & Cons Generation Complete")
print(f"Companies : {df['company_id'].nunique()}")
print(f"Statements: {len(output)}")
print("=" * 50)
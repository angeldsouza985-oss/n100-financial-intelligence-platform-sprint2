import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    year,
    operating_activity,
    investing_activity,
    financing_activity
FROM financial_ratios
"""

df = pd.read_sql(query, conn)

def sign(value):
    if value > 0:
        return "+"
    elif value < 0:
        return "-"
    return "0"

def classify(cfo, cfi, cff):
    pattern = (sign(cfo), sign(cfi), sign(cff))

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    return mapping.get(pattern, "Other")

df["cfo_sign"] = df["operating_activity"].apply(sign)
df["cfi_sign"] = df["investing_activity"].apply(sign)
df["cff_sign"] = df["financing_activity"].apply(sign)

df["pattern_label"] = df.apply(
    lambda row: classify(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
    ),
    axis=1,
)

os.makedirs("output", exist_ok=True)

df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
].to_csv(
    "output/capital_allocation.csv",
    index=False,
)

conn.close()

print("capital_allocation.csv generated successfully.")
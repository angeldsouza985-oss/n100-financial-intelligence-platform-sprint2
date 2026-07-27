import os
import sqlite3
import pandas as pd

OUTPUT_DIR = "output"

capital = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "capital_allocation.csv"
    )
)

cashflow = pd.read_excel(
    os.path.join(
        OUTPUT_DIR,
        "cashflow_intelligence.xlsx"
    )
)

# -----------------------------
# Latest year for each company
# -----------------------------

capital["year_num"] = (
    capital["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(float)
)

latest = (
    capital.sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

# -----------------------------
# Distribution Summary
# -----------------------------

distribution = (
    latest.groupby("pattern_label")
    .size()
    .reset_index(name="company_count")
)

distribution.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "capital_pattern_distribution.csv"
    ),
    index=False,
)

# -----------------------------
# Add Capital Allocation Label
# -----------------------------

cashflow = cashflow.merge(
    latest[
        [
            "company_id",
            "pattern_label"
        ]
    ],
    on="company_id",
    how="left"
)

cashflow.rename(
    columns={
        "pattern_label":
        "capital_allocation_pattern"
    },
    inplace=True,
)

cashflow.to_excel(
    os.path.join(
        OUTPUT_DIR,
        "cashflow_intelligence.xlsx"
    ),
    index=False,
)

# -----------------------------
# Pattern Changes
# -----------------------------

changes = []

for company, grp in capital.groupby("company_id"):

    grp = grp.sort_values("year_num")

    previous = None

    for _, row in grp.iterrows():

        current = row["pattern_label"]

        if previous is not None and previous != current:

            changes.append({

                "company_id": company,

                "year": row["year"],

                "from_pattern": previous,

                "to_pattern": current,

            })

        previous = current

changes = pd.DataFrame(changes)

changes.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "pattern_changes.csv"
    ),
    index=False,
)

print("=" * 50)
print("Capital Allocation Report Complete")
print(f"Companies : {latest['company_id'].nunique()}")
print(f"Patterns  : {distribution.shape[0]}")
print(f"Changes   : {len(changes)}")
print("=" * 50)
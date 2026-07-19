import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

ratios = pd.read_sql(
    "SELECT DISTINCT company_id FROM financial_ratios",
    conn
)

peers = pd.read_sql(
    "SELECT company_id FROM peer_groups",
    conn
)

missing = ratios[
    ~ratios["company_id"].isin(peers["company_id"])
]

print(missing)

print("\nMissing companies:", len(missing))

conn.close()
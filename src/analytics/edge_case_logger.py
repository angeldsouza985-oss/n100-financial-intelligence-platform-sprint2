import sqlite3
import os

DB_PATH = "nifty100.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

os.makedirs("output", exist_ok=True)

query = """
SELECT
    c.company_name,
    fr.year,
    fr.return_on_equity_pct,
    c.roe_percentage,
    fr.return_on_capital_employed_pct,
    c.roce_percentage
FROM financial_ratios fr
JOIN companies c
ON fr.company_id = c.id
"""

rows = cur.execute(query).fetchall()

with open("output/ratio_edge_cases.log", "w") as log:

    log.write("SPRINT 2 EDGE CASE REPORT\n")
    log.write("=" * 50 + "\n\n")

    for row in rows:

        company = row[0]
        year = row[1]

        calc_roe = row[2]
        source_roe = row[3]

        calc_roce = row[4]
        source_roce = row[5]

        if (
            calc_roe is not None
            and source_roe is not None
        ):

            diff = abs(calc_roe - source_roe)

            if diff > 5:

                log.write(
                    f"{company} ({year})\n"
                )

                log.write(
                    f"ROE Difference : {diff:.2f}%\n"
                )

                log.write(
                    "Category : Data Source Issue\n\n"
                )

        if (
            calc_roce is not None
            and source_roce is not None
        ):

            diff = abs(calc_roce - source_roce)

            if diff > 5:

                log.write(
                    f"{company} ({year})\n"
                )

                log.write(
                    f"ROCE Difference : {diff:.2f}%\n"
                )

                log.write(
                    "Category : Formula Difference\n\n"
                )

conn.close()

print("=" * 50)
print("ratio_edge_cases.log generated")
print(f"Rows Checked : {len(rows)}")
print("=" * 50)
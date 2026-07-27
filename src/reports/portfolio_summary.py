import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB = "nifty100.db"

OUTPUT = "reports/portfolio"

os.makedirs(OUTPUT, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT
    s.company_id,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.pe_ratio,
    fr.pb_ratio,
    fr.debt_to_equity,
    fr.free_cash_flow

FROM sectors s

JOIN financial_ratios fr
ON s.company_id = fr.company_id

WHERE fr.merge_year = 2024

ORDER BY s.company_id
""", conn)

conn.close()

pdf = SimpleDocTemplate(
    os.path.join(
        OUTPUT,
        "portfolio_summary.pdf"
    )
)

story = []

for _, row in df.iterrows():

    story.append(
        Paragraph(
            f"<b><font size=18>{row['company_id']}</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Sector: {row['broad_sector']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    table = Table([

        ["Metric", "Value"],

        ["ROE", f"{row['return_on_equity_pct']:.2f}%"],

        ["ROCE", f"{row['return_on_capital_employed_pct']:.2f}%"],

        ["P/E", f"{row['pe_ratio']:.2f}"],

        ["P/B", f"{row['pb_ratio']:.2f}"],

        ["Debt / Equity", f"{row['debt_to_equity']:.2f}"],

        ["Free Cash Flow", f"{row['free_cash_flow']:,.0f}"],

    ])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.navy),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BOTTOMPADDING", (0,0), (-1,0), 8),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ])

    )

    story.append(table)

    story.append(PageBreak())

pdf.build(story)

print("=" * 50)
print("Portfolio Summary Complete")
print(f"Companies : {len(df)}")
print("=" * 50)
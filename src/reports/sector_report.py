import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB = "nifty100.db"

OUTPUT = "reports/sector"

os.makedirs(OUTPUT, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT
    s.company_id,
    s.broad_sector,
    s.sub_sector,
    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.debt_to_equity,
    fr.pe_ratio,
    fr.pb_ratio,
    fr.free_cash_flow,
    fr.revenue_cagr_5yr
FROM sectors s
JOIN financial_ratios fr
ON s.company_id = fr.company_id
WHERE fr.merge_year=2024
""", conn)

conn.close()
def generate_sector_report(sector_name):

    sector_df = df[
        df["broad_sector"] == sector_name
    ].copy()

    if sector_df.empty:
        return

    filename = os.path.join(
        OUTPUT,
        f"{sector_name}_report.pdf"
    )

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            f"<b><font size=20>{sector_name} Sector Report</font></b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Total Companies:</b> {len(sector_df)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    summary = [

        ["Metric", "Median"],

        [
            "ROE %",
            f"{sector_df['return_on_equity_pct'].median():.2f}"
        ],

        [
            "ROCE %",
            f"{sector_df['return_on_capital_employed_pct'].median():.2f}"
        ],

        [
            "Net Profit Margin %",
            f"{sector_df['net_profit_margin_pct'].median():.2f}"
        ],

        [
            "Debt / Equity",
            f"{sector_df['debt_to_equity'].median():.2f}"
        ],

        [
            "P/E",
            f"{sector_df['pe_ratio'].median():.2f}"
        ],

        [
            "P/B",
            f"{sector_df['pb_ratio'].median():.2f}"
        ],

        [
            "Revenue CAGR %",
            f"{sector_df['revenue_cagr_5yr'].median():.2f}"
        ],

    ]

    table = Table(summary)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Company KPI Summary</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    company_table = [[
        "Company",
        "ROE",
        "ROCE",
        "P/E",
        "P/B",
        "D/E",
        "Revenue CAGR"
    ]]

    for _, row in sector_df.sort_values("company_id").iterrows():

        company_table.append([

            row["company_id"],

            f"{row['return_on_equity_pct']:.2f}",

            f"{row['return_on_capital_employed_pct']:.2f}",

            f"{row['pe_ratio']:.2f}",

            f"{row['pb_ratio']:.2f}",

            f"{row['debt_to_equity']:.2f}",

            f"{row['revenue_cagr_5yr']:.2f}",

        ])

    table = Table(company_table, repeatRows=1)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.navy),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("FONTSIZE", (0, 0), (-1, -1), 8),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("WORDWRAP", (0, 0), (-1, -1), True),

        ])

    )

    story.append(table)

    pdf.build(story)
    # ==========================================
# Generate Reports for All Sectors
# ==========================================

sectors = sorted(df["broad_sector"].dropna().unique())

count = 0

for sector in sectors:
    generate_sector_report(sector)
    count += 1

print("=" * 50)
print("Sector Report Generation Complete")
print(f"Sector PDFs Generated : {count}")
print("=" * 50)
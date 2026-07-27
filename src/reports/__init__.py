import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB = "nifty100.db"

OUTPUT = "reports/tearsheets"

RADAR = "reports/radar_charts"

os.makedirs(OUTPUT, exist_ok=True)

styles = getSampleStyleSheet()


conn = sqlite3.connect(DB)

ratios = pd.read_sql(
"""
SELECT *
FROM financial_ratios
WHERE merge_year=2024
""",
conn
)

sectors = pd.read_sql(
"""
SELECT *
FROM sectors
""",
conn
)

pros = pd.read_csv(
"output/pros_cons_generated.csv"
)

cash = pd.read_excel(
"output/cashflow_intelligence.xlsx"
)

conn.close()


def generate_tearsheet(company):

    r = ratios[
        ratios.company_id == company
    ]

    if r.empty:
        return

    r = r.iloc[0]

    s = sectors[
        sectors.company_id == company
    ]

    sector = ""

    if not s.empty:
        sector = s.iloc[0]["broad_sector"]

    filename = os.path.join(
        OUTPUT,
        f"{company}_tearsheet.pdf"
    )

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            f"<b><font size=18>{company}</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Sector : {sector}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1,12)
    )

    table = Table(
        [

            ["Metric","Value"],

            ["ROE",f"{r.return_on_equity_pct:.2f}%"],

            ["ROCE",f"{r.return_on_capital_employed_pct:.2f}%"],

            ["P/E",f"{r.pe_ratio:.2f}"],

            ["P/B",f"{r.pb_ratio:.2f}"],

            ["Debt/Equity",f"{r.debt_to_equity:.2f}"],

            ["FCF",f"{r.free_cash_flow:,.0f}"],

        ]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.navy),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

        ])

    )

    story.append(table)

    story.append(
        Spacer(1,18)
    )

    radar = os.path.join(
        RADAR,
        f"{company}_radar.png"
    )

    if os.path.exists(radar):

        story.append(Image(radar,width=320,height=320))

    story.append(
        Spacer(1,15)
    )

    story.append(
        Paragraph("<b>Pros</b>",styles["Heading2"])
    )

    p = pros[
        (pros.company_id==company)
        &
        (pros.type=="Pro")
    ]

    for _,row in p.iterrows():

        story.append(
            Paragraph(
                "• "+row["text"],
                styles["BodyText"]
            )
        )

    story.append(
        Spacer(1,10)
    )

    story.append(
        Paragraph("<b>Cons</b>",styles["Heading2"])
    )

    c = pros[
        (pros.company_id==company)
        &
        (pros.type=="Con")
    ]

    for _,row in c.iterrows():

        story.append(
            Paragraph(
                "• "+row["text"],
                styles["BodyText"]
            )
        )

    cf = cash[
        cash.company_id==company
    ]

    if not cf.empty:

        cf = cf.iloc[0]

        story.append(
            Spacer(1,12)
        )

        story.append(
            Paragraph(
                f"<b>Capital Allocation:</b> {cf['capital_allocation_pattern']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>CFO Quality:</b> {cf['cfo_quality_label']}",
                styles["Normal"]
            )
        )

    pdf.build(story)


companies = sorted(
    ratios.company_id.unique()
)

count = 0

for company in companies:

    generate_tearsheet(company)

    count += 1

print("="*50)

print("Company Tearsheet Generation Complete")

print("PDFs Generated :",count)

print("="*50)
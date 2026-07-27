from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/portfolio/summary")
def portfolio_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(DISTINCT company_id) AS total_companies,
            ROUND(AVG(return_on_equity_pct),2) AS avg_roe,
            ROUND(AVG(return_on_capital_employed_pct),2) AS avg_roce,
            ROUND(AVG(pe_ratio),2) AS avg_pe,
            ROUND(AVG(debt_to_equity),2) AS avg_de,
            ROUND(AVG(revenue_cagr_5yr),2) AS avg_revenue_cagr,
            ROUND(AVG(free_cash_flow),2) AS avg_fcf
        FROM financial_ratios
        WHERE merge_year = 2024
    """)

    row = cursor.fetchone()

    conn.close()

    return dict(row)
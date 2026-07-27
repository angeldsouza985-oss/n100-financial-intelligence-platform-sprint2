from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/companies")
def get_companies():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            broad_sector,
            sub_sector
        FROM sectors
        ORDER BY company_id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.company_id,
            s.broad_sector,
            s.sub_sector,
            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.debt_to_equity,
            fr.pe_ratio,
            fr.pb_ratio,
            fr.free_cash_flow,
            fr.revenue_cagr_5yr
        FROM sectors s
        LEFT JOIN financial_ratios fr
            ON s.company_id = fr.company_id
        WHERE
            s.company_id = ?
            AND fr.merge_year = 2024
    """, (ticker.upper(),))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return dict(row)


@router.get("/companies/{ticker}/ratios")
def get_ratios(ticker: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            merge_year,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            net_profit_margin_pct,
            debt_to_equity,
            pe_ratio,
            pb_ratio,
            revenue_cagr_5yr,
            free_cash_flow
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY merge_year
    """, (ticker.upper(),))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Company not found")

    return [dict(r) for r in rows]
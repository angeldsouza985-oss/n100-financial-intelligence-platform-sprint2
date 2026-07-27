from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/peers/{ticker}")
def get_peers(ticker: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT broad_sector
        FROM sectors
        WHERE company_id = ?
    """, (ticker.upper(),))

    sector = cursor.fetchone()

    if sector is None:
        conn.close()
        return {"error": "Company not found"}

    sector = sector["broad_sector"]

    cursor.execute("""
        SELECT
            s.company_id,
            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.debt_to_equity,
            fr.pe_ratio,
            fr.pb_ratio,
            fr.free_cash_flow
        FROM sectors s
        JOIN financial_ratios fr
            ON s.company_id = fr.company_id
        WHERE
            s.broad_sector = ?
            AND fr.merge_year = 2024
        ORDER BY fr.return_on_equity_pct DESC
    """, (sector,))

    rows = cursor.fetchall()

    conn.close()

    return {
        "sector": sector,
        "companies": [dict(r) for r in rows]
    }
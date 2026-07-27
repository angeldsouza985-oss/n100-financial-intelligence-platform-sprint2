from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/valuation/{ticker}")
def valuation(ticker: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            pe_ratio,
            pb_ratio,
            market_cap_crore,
            dividend_yield_pct
        FROM financial_ratios
        WHERE
            company_id=?
            AND merge_year=2024
    """, (ticker.upper(),))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {"error": "Company not found"}

    data = dict(row)

    # Simple valuation labels
    if data["pe_ratio"] is None:
        label = "Unknown"
    elif data["pe_ratio"] < 20:
        label = "Undervalued"
    elif data["pe_ratio"] < 40:
        label = "Fairly Valued"
    else:
        label = "Expensive"

    data["valuation_label"] = label

    return data
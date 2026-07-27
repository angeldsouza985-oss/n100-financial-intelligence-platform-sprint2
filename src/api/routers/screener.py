from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/screener")
def screener(

    roe_min: float = 0,
    de_max: float = 999,
    fcf_min: float = -999999999,
    revenue_cagr_min: float = -999,
    pe_max: float = 999999,

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            company_id,

            return_on_equity_pct,

            debt_to_equity,

            free_cash_flow,

            revenue_cagr_5yr,

            pe_ratio,

            pb_ratio,

            operating_profit_margin_pct,

            net_profit_margin_pct

        FROM financial_ratios

        WHERE

            merge_year=2024

            AND return_on_equity_pct>=?

            AND debt_to_equity<=?

            AND free_cash_flow>=?

            AND revenue_cagr_5yr>=?

            AND (
                pe_ratio<=?
                OR pe_ratio IS NULL
            )

        ORDER BY return_on_equity_pct DESC
        """,

        (
            roe_min,
            de_max,
            fcf_min,
            revenue_cagr_min,
            pe_max,
        ),

    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(r) for r in rows]
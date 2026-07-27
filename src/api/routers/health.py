import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

DB = "nifty100.db"


@router.get("/health")
def health():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    tables = [

        "financial_ratios",

        "market_cap",

        "peer_groups",

        "peer_percentiles",

        "sectors",

    ]

    counts = {}

    for table in tables:

        try:

            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            counts[table] = cursor.fetchone()[0]

        except:

            counts[table] = None

    conn.close()

    return {

        "status": "ok",

        "version": "1.0.0",

        "uptime_seconds": round(
            time.time() - START_TIME,
            2,
        ),

        "db_row_counts": counts,

    }
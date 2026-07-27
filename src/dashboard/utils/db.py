import sqlite3
import pandas as pd
import streamlit as st

DB = "nifty100.db"


@st.cache_data(ttl=600)
def query(sql):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# ==========================================
# Financial Ratios
# ==========================================

def get_ratios(year=None):

    sql = "SELECT * FROM financial_ratios"

    if year is not None:
        sql += f" WHERE merge_year={year}"

    return query(sql)


# ==========================================
# Sectors
# ==========================================

def get_sectors():

    return query("""
        SELECT *
        FROM sectors
    """)


# ==========================================
# Companies
# ==========================================

def get_companies():

    return query("""
        SELECT DISTINCT company_id
        FROM financial_ratios
        ORDER BY company_id
    """)


# ==========================================
# Peer Percentiles
# ==========================================

def get_peers():

    return query("""
        SELECT *
        FROM peer_percentiles
    """)


# ==========================================
# Market Cap
# ==========================================

def get_market_cap():

    return query("""
        SELECT *
        FROM market_cap
    """)


# ==========================================
# Peer Groups
# ==========================================

def get_peer_groups():

    return query("""
        SELECT DISTINCT
            peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
    """)


# ==========================================
# Peer Companies
# ==========================================

def get_peer_companies(group_name, year=2024):

    sql = f"""
        SELECT
            pg.company_id,
            pg.is_benchmark,

            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.net_profit_margin_pct,
            fr.pe_ratio,
            fr.pb_ratio,
            fr.debt_to_equity,
            fr.operating_profit_margin_pct,
            fr.revenue_cagr_5yr,
            fr.pat_cagr_5yr,
            fr.free_cash_flow

        FROM peer_groups pg

        INNER JOIN financial_ratios fr
            ON pg.company_id = fr.company_id

        WHERE
            pg.peer_group_name = '{group_name}'
            AND fr.merge_year = {year}

        ORDER BY
            pg.is_benchmark DESC,
            fr.return_on_equity_pct DESC
    """

    return query(sql)

@st.cache_data(ttl=600)
def get_company_trend(company):

    sql = f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{company}'
        ORDER BY merge_year
    """

    return query(sql)

@st.cache_data(ttl=600)
def get_sector_data(year=2024):

    sql = f"""
        SELECT
            s.broad_sector,
            s.company_id,

            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.net_profit_margin_pct,
            fr.market_cap_crore,
            fr.pe_ratio,
            fr.pb_ratio,
            fr.debt_to_equity

        FROM sectors s

        INNER JOIN financial_ratios fr
            ON s.company_id = fr.company_id

        WHERE fr.merge_year = {year}
    """

    return query(sql)
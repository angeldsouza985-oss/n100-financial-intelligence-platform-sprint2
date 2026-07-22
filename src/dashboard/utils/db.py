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


def get_ratios(year=None):

    sql = "SELECT * FROM financial_ratios"

    if year is not None:
        sql += f" WHERE merge_year={year}"

    return query(sql)


def get_sectors():

    return query("""
        SELECT *
        FROM sectors
    """)


def get_companies():

    return query("""
        SELECT DISTINCT
            company_id
        FROM financial_ratios
        ORDER BY company_id
    """)


def get_peers():

    return query("""
        SELECT *
        FROM peer_percentiles
    """)


def get_market_cap():

    return query("""
        SELECT *
        FROM market_cap
    """)
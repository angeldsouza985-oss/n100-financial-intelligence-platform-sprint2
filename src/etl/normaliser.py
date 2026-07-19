"""
Sprint 1 - Data Normalisation
"""


def normalize_ticker(ticker):

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker

def normalize_year(year):
    """
    Normalize year values.

    Examples:
    'Mar 2024' -> 2024
    'Dec 2023' -> 2023
    'TTM' -> 'TTM'
    """

    if year is None:
        return None

    year = str(year).strip()

    if year.upper() == "TTM":
        return "TTM"

    import re

    match = re.search(r"\d{4}", year)

    if match:
        return match.group()

    return None
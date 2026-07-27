import pandas as pd

files = [
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

for file in files:

    header = 1 if file in [
        "analysis.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "companies.xlsx",
        "documents.xlsx",
        "profitandloss.xlsx",
        "prosandcons.xlsx"
    ] else 0

    df = pd.read_excel(
        f"data/raw/{file}",
        header=header
    )

    print("\n" + "="*50)
    print(file)
    print(df.columns.tolist())
import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

peers = pd.read_sql("""
SELECT *
FROM peer_groups
""", conn)

conn.close()

df = df.merge(
    peers,
    on="company_id",
    how="inner"
)

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "asset_turnover",
]

os.makedirs(
    "reports/radar_charts",
    exist_ok=True,
)

print("Generating radar charts...")
for company in df["company_id"].unique():

    company_df = df[df["company_id"] == company]

    latest = company_df.sort_values(
        "merge_year"
    ).iloc[-1]

    group = latest["peer_group_name"]

    peer_avg = (
        df[df["peer_group_name"] == group]
        .groupby("peer_group_name")[metrics]
        .mean()
        .iloc[0]
    )

    company_values = latest[metrics].fillna(0).tolist()
    peer_values = peer_avg.fillna(0).tolist()

    labels = metrics

    N = len(labels)

    angles = np.linspace(
        0,
        2 * np.pi,
        N,
        endpoint=False
    ).tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]
    angles += angles[:1]

    plt.figure(figsize=(7,7))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(company)

    plt.legend()

    plt.savefig(
        f"reports/radar_charts/{company}_radar.png"
    )

    plt.close()

print("\nRadar charts generated successfully!")
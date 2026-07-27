import os
import sqlite3
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

DB = "nifty100.db"

OUTPUT = "output"
REPORTS = "reports"

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)

conn = sqlite3.connect(DB)

df = pd.read_sql("""
SELECT
    s.company_id,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.revenue_cagr_5yr,
    fr.free_cash_flow,
    fr.operating_profit_margin_pct

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.merge_year = 2024
""", conn)

conn.close()

features = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "free_cash_flow",

    "operating_profit_margin_pct",

]

# -----------------------------
# Sector Median Imputation
# -----------------------------

for col in features:
    df[col] = (
        df.groupby("broad_sector")[col]
        .transform(lambda x: x.fillna(x.median()))
    )

# Fill any remaining NaN values (e.g. Unknown sector)
for col in features:
    df[col] = df[col].fillna(df[col].median())

imputer = SimpleImputer(strategy="median")

X = imputer.fit_transform(
    df[features]
)

# -----------------------------
# Scaling
# -----------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# -----------------------------
# Elbow Plot
# -----------------------------

inertia = []

for k in range(2,11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10,
    )

    model.fit(X_scaled)

    inertia.append(
        model.inertia_
    )

plt.figure(figsize=(6,4))

plt.plot(
    range(2,11),
    inertia,
    marker="o",
)

plt.xlabel("Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Plot")

plt.grid(True)

plt.savefig(
    "reports/elbow_plot.png",
    dpi=200,
    bbox_inches="tight",
)

plt.close()

# -----------------------------
# Final Model
# -----------------------------

model = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10,
)

labels = model.fit_predict(X_scaled)

distance = model.transform(
    X_scaled
).min(axis=1)

names = {

    0:"High-Quality Compounders",

    1:"Emerging Growth",

    2:"Value Cyclicals",

    3:"Defensive Dividend",

    4:"Turnaround",

}

df["cluster_id"] = labels

df["cluster_name"] = (
    df["cluster_id"]
    .map(names)
)

df["distance_from_centroid"] = (
    distance.round(3)
)

output = df[

    [

        "company_id",

        "cluster_id",

        "cluster_name",

        "distance_from_centroid",

    ]

]

output.to_csv(

    "output/cluster_labels.csv",

    index=False,

)

print("="*50)
print("KMeans Clustering Complete")
print("Companies :",len(output))
print("Clusters  :",output.cluster_id.nunique())
print("="*50)
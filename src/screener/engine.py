import os
import sys
import sqlite3
import pandas as pd
import yaml

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("Current file:", __file__)
print("Project root:", PROJECT_ROOT)

from src.screener.scoring import compute_quality_score
from openpyxl import Workbook

class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect("nifty100.db")

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        with open(
            "src/screener/screener_config.yaml",
            "r"
        ) as file:
            self.config = yaml.safe_load(file)

    def quality_compounder(self):
        return self.apply_filter("quality_compounder")

    def value_pick(self):
        return self.apply_filter("value_pick")

    def growth_accelerator(self):
        return self.apply_filter("growth_accelerator")

    def dividend_champion(self):
        return self.apply_filter("dividend_champion")

    def debt_free_bluechip(self):
        return self.apply_filter("debt_free_bluechip")

    def turnaround_watch(self):
        return self.apply_filter("turnaround_watch")

    def apply_filter(self, preset):
        

        data = self.df.copy()
        # Keep only the latest record for each company
        data = (
            data.sort_values("year")
            .drop_duplicates(subset="company_id", keep="last")
        )

        rules = self.config[preset]

        for metric, value in rules.items():

            if metric.endswith("_min"):

                column = metric.replace("_min", "")

                if column in data.columns:

                    data = data[
                        data[column] >= value
                    ]

            elif metric.endswith("_max"):

                column = metric.replace("_max", "")

                if column in data.columns:

                    data = data[
                        data[column] <= value
                    ]

        return data
    

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    engine = ScreenerEngine()

    presets = {
        "Quality Compounder": engine.quality_compounder,
        "Value Pick": engine.value_pick,
        "Growth Accelerator": engine.growth_accelerator,
        "Dividend Champion": engine.dividend_champion,
        "Debt-Free Blue Chip": engine.debt_free_bluechip,
        "Turnaround Watch": engine.turnaround_watch,
    }

    wb = Workbook()

    # Remove the default sheet
    wb.remove(wb.active)

    for name, func in presets.items():

        result = func()

        result = compute_quality_score(result)

        result = result.sort_values(
            "composite_quality_score",
            ascending=False,
        )

        print(f"\n{name}")
        print(f"Companies Returned: {len(result)}")

        print(
            result[
                [
                    "company_id",
                    "composite_quality_score",
                ]
            ].head(10)
        )

        # Create worksheet
        ws = wb.create_sheet(title=name[:31])

        # Write headers
        ws.append(list(result.columns))

        # Write data
        for row in result.itertuples(index=False):
            ws.append(list(row))

    import os

    os.makedirs("output", exist_ok=True)

    wb.save("output/screener_output.xlsx")

    print("\n✅ screener_output.xlsx generated successfully!")

    engine.close()
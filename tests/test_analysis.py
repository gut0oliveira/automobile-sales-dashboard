from pathlib import Path
import sys
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import build_summary, create_charts


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame(
            {
                "Date": pd.to_datetime(["2020-01-01", "2020-02-01", "2021-01-01"]),
                "Year": [2020, 2020, 2021],
                "Recession": [1, 1, 0],
                "Advertising_Expenditure": [100, 200, 300],
                "unemployment_rate": [8.0, 9.0, 4.0],
                "Automobile_Sales": [50.0, 70.0, 120.0],
                "Vehicle_Type": ["A", "B", "A"],
            }
        )

    def test_summary_uses_correct_aggregations(self):
        summary = build_summary(self.frame).set_index("metric")["value"]
        self.assertEqual(summary["records"], 3)
        self.assertEqual(summary["average_sales_recession"], 60.0)
        self.assertEqual(summary["average_sales_non_recession"], 120.0)
        self.assertEqual(summary["recession_sales_difference_percent"], -50.0)
        self.assertEqual(summary["top_vehicle_type_during_recession"], "B")

    def test_charts_are_generated(self):
        from tempfile import TemporaryDirectory

        temp_root = ROOT / ".tmp"
        temp_root.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=temp_root) as directory:
            output = Path(directory)
            create_charts(self.frame, output)
            self.assertGreater((output / "annual_sales_trend.png").stat().st_size, 0)
            self.assertGreater(
                (output / "sales_by_vehicle_and_period.png").stat().st_size, 0
            )


if __name__ == "__main__":
    unittest.main()

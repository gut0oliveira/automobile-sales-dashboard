"""Reproduce the portfolio analysis for the automobile-sales dataset."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)
DATA_PATH = ROOT / "data" / "historical_automobile_sales.csv"
REPORT_PATH = ROOT / "reports" / "analysis_summary.csv"
IMAGE_DIR = ROOT / "images"
REQUIRED_COLUMNS = {
    "Date",
    "Year",
    "Recession",
    "Advertising_Expenditure",
    "unemployment_rate",
    "Automobile_Sales",
    "Vehicle_Type",
}


def download_dataset(path: Path = DATA_PATH) -> Path:
    """Download the course dataset only when it is not cached locally."""
    if path.exists():
        return path
    response = requests.get(DATA_URL, timeout=60)
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return path


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    frame = pd.read_csv(download_dataset(path))
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    frame = frame.copy()
    frame["Date"] = pd.to_datetime(frame["Date"], errors="raise")
    return frame


def build_summary(frame: pd.DataFrame) -> pd.DataFrame:
    recession = frame.loc[frame["Recession"].eq(1)]
    regular = frame.loc[frame["Recession"].eq(0)]
    if recession.empty or regular.empty:
        raise ValueError("Dataset must contain recession and non-recession records.")

    recession_average = recession["Automobile_Sales"].mean()
    regular_average = regular["Automobile_Sales"].mean()
    top_recession_vehicle = (
        recession.groupby("Vehicle_Type")["Automobile_Sales"].mean().idxmax()
    )
    annual = frame.groupby("Year")["Automobile_Sales"].mean()

    rows = [
        ("records", len(frame)),
        ("start_date", frame["Date"].min().date().isoformat()),
        ("end_date", frame["Date"].max().date().isoformat()),
        ("average_sales_recession", round(recession_average, 2)),
        ("average_sales_non_recession", round(regular_average, 2)),
        (
            "recession_sales_difference_percent",
            round((recession_average / regular_average - 1) * 100, 2),
        ),
        ("top_vehicle_type_during_recession", top_recession_vehicle),
        ("highest_average_sales_year", int(annual.idxmax())),
        ("lowest_average_sales_year", int(annual.idxmin())),
        (
            "recession_unemployment_sales_correlation",
            round(recession["unemployment_rate"].corr(recession["Automobile_Sales"]), 4),
        ),
    ]
    return pd.DataFrame(rows, columns=["metric", "value"])


def create_charts(frame: pd.DataFrame, output_dir: Path = IMAGE_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    annual = frame.groupby("Year", as_index=False)["Automobile_Sales"].mean()
    fig, ax = plt.subplots(figsize=(11, 5.5))
    sns.lineplot(data=annual, x="Year", y="Automobile_Sales", ax=ax, color="#2563eb")
    ax.set(title="Average automobile sales by year", ylabel="Average sales", xlabel="Year")
    fig.tight_layout()
    fig.savefig(output_dir / "annual_sales_trend.png", dpi=160)
    plt.close(fig)

    comparison = (
        frame.assign(Period=frame["Recession"].map({0: "Non-recession", 1: "Recession"}))
        .groupby(["Vehicle_Type", "Period"], as_index=False)["Automobile_Sales"]
        .mean()
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(
        data=comparison,
        x="Vehicle_Type",
        y="Automobile_Sales",
        hue="Period",
        palette=["#2563eb", "#dc2626"],
        ax=ax,
    )
    ax.set(
        title="Average sales by vehicle type and economic period",
        ylabel="Average sales",
        xlabel="Vehicle type",
    )
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(output_dir / "sales_by_vehicle_and_period.png", dpi=160)
    plt.close(fig)


def main() -> None:
    frame = load_data()
    summary = build_summary(frame)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(REPORT_PATH, index=False)
    create_charts(frame)
    print(summary.to_string(index=False))
    print(f"\nReport: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Charts: {IMAGE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

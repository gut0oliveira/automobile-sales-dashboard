# Automobile Sales Dashboard

How do automobile sales vary across years, vehicle categories, and recession periods?

An educational IBM Data Visualization project combining an exploratory notebook with an interactive Plotly Dash dashboard. The course dataset represents the fictional XYZAutomotives scenario; it is not evidence about a real company's performance.

## Explore the dashboard

- **Yearly Statistics:** average sales across all years, monthly averages for the selected year, sales by vehicle type, and total advertising expenditure by category.
- **Recession Period Statistics:** sales averages during recession years, vehicle categories, advertising shares, and the relationship between unemployment and sales. The year selector is disabled in this mode.

Sales charts show averages, while advertising charts sum expenditure. These descriptive associations do not establish that recession or unemployment caused a change in sales. The annual overview always shows all years; the other yearly charts follow the selected year.

## Run locally

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe dashboard/app.py
```

Open http://127.0.0.1:8050 and stop the server with Ctrl+C.

The first start downloads the course CSV over HTTPS. Later starts use the cached file in `data/` (ignored by Git). The app resolves this path relative to its source file.

## Files

- [Dashboard](dashboard/app.py): interactive reports and data loading.
- [Exploratory notebook](notebooks/automobile_sales_analysis.ipynb): original course analysis, preserved with its outputs.
- [Dependencies](requirements.txt): dashboard and notebook packages.

Select the project's `.venv` kernel in VS Code to inspect the notebook. Its original cells have not been modernized or re-executed as part of the dashboard migration.

## Dataset and attribution

The dataset URL is defined in `DATA_URL` in the dashboard and points to IBM Skills Network's `historical_automobile_sales.csv`. Available years are derived from the downloaded data.

The notebook retains IBM course instructions and attribution. The repository's [MIT license](LICENSE) applies to original contributions; third-party educational material and data retain their own terms.

## Technologies

Python, Pandas, Plotly, Dash, Matplotlib, Seaborn, Folium and Jupyter.

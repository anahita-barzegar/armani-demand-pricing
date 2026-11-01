"""
03 - Dynamic Pricing Strategy
Armani Middle East Trading
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine

# =========================================================
# 1. Load data from PostgreSQL
# =========================================================
DB_URL = "postgresql+psycopg2://armani:armani123@localhost:5432/armani_trading"

engine = create_engine(DB_URL)
df = pd.read_sql("SELECT * FROM vw_sales_enriched ORDER BY product_name, week_key", engine)

print("Data loaded:", df.shape)
print(df.head(3))

# Load forecast if available
fc_path = Path("data/processed/demand_forecast_26w.csv")
forecast_df = pd.read_csv(fc_path) if fc_path.exists() else None
if forecast_df is not None:
    print("Forecast loaded:", forecast_df.shape)
else:
    print("No forecast file found – will use recent sales as proxy")

# =========================================================
# 2. Pricing Rules Configuration
# =========================================================
MIN_MARGIN = 0.18          # 18% minimum gross margin
MAX_PRICE_UPLIFT = 1.12    # max +12% vs current price
DEMAND_LOOKBACK = 4        # weeks

def demand_factor(forecast: float, recent_sales: float) -> float:
    if recent_sales <= 0:
        return 1.0
    ratio = forecast / recent_sales

    if ratio > 1.20:
        return 1.08
    elif ratio > 1.05:
        return 1.04
    elif ratio >= 0.90:
        return 1.00
    elif ratio >= 0.75:
        return 0.97
    else:
        return 0.94


def inventory_factor(inventory: float, recent_sales: float) -> float:
    if recent_sales <= 0:
        return 1.0
    weeks_of_cover = inventory / recent_sales

    if weeks_of_cover > 8:
        return 0.95
    elif weeks_of_cover > 4:
        return 0.99
    elif weeks_of_cover > 1.5:
        return 1.02
    else:
        return 1.06


def seasonality_factor(week_of_year: int) -> float:
    if week_of_year in list(range(10, 21)) + list(range(40, 49)):
        return 1.03      # peak
    elif week_of_year in list(range(25, 36)):
        return 0.98      # off-peak
    return 1.00


def apply_guardrails(new_price: float, base_price: float, cogs: float) -> float:
    min_price = cogs * (1 + MIN_MARGIN)
    max_price = base_price * MAX_PRICE_UPLIFT
    return float(np.clip(new_price, min_price, max_price))


# =========================================================
# 3. Prepare latest snapshot per product
# =========================================================
latest = (
    df.sort_values("week_key")
      .groupby("product_name", as_index=False)
      .tail(1)
      .copy()
)

# Recent average sales
recent = (
    df.groupby("product_name")["sales_units"]
      .apply(lambda x: x.tail(DEMAND_LOOKBACK).mean())
      .rename("recent_sales")
      .reset_index()
)
latest = latest.merge(recent, on="product_name", how="left")

# Attach forecast
if forecast_df is not None and not forecast_df.empty:
    fc = (
        forecast_df.groupby("product_name")["predicted_demand"]
                   .mean()
                   .rename("forecast_demand")
                   .reset_index()
    )
    latest = latest.merge(fc, on="product_name", how="left")
else:
    latest["forecast_demand"] = latest["recent_sales"]

latest["forecast_demand"] = latest["forecast_demand"].fillna(latest["recent_sales"])
latest["recent_sales"] = latest["recent_sales"].fillna(latest["sales_units"])

# Week of year
if "week_of_year" not in latest.columns:
    latest["week_of_year"] = ((latest["week_key"] - 1) % 52) + 1

# =========================================================
# 4. Apply Dynamic Pricing Engine
# =========================================================
latest["f_demand"] = latest.apply(
    lambda r: demand_factor(r["forecast_demand"], r["recent_sales"]), axis=1
)
latest["f_inventory"] = latest.apply(
    lambda r: inventory_factor(r["inventory_level"], r["recent_sales"]), axis=1
)
latest["f_season"] = latest["week_of_year"].apply(seasonality_factor)

latest["raw_new_price"] = (
    latest["price_per_unit"]
    * latest["f_demand"]
    * latest["f_inventory"]
    * latest["f_season"]
)

latest["recommended_price"] = latest.apply(
    lambda r: apply_guardrails(
        r["raw_new_price"],
        r["price_per_unit"],
        r["cogs"]
    ),
    axis=1
)

latest["price_change_pct"] = (
    (latest["recommended_price"] - latest["price_per_unit"])
    / latest["price_per_unit"]
    * 100
).round(2)

# =========================================================
# 5. Results
# =========================================================
result = latest[[
    "product_name",
    "week_key",
    "price_per_unit",
    "cogs",
    "inventory_level",
    "recent_sales",
    "forecast_demand",
    "f_demand",
    "f_inventory",
    "f_season",
    "recommended_price",
    "price_change_pct"
]].copy()

result = result.rename(columns={"price_per_unit": "current_price"})

print("\n=== Dynamic Pricing Recommendations ===")
print(result.to_string(index=False))

# Save
out_path = Path("data/processed/dynamic_pricing_recommendations.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(out_path, index=False)
print(f"\nSaved to: {out_path}")

# =========================================================
# 6. Summary Insights
# =========================================================
print("\n=== Summary ===")
print(f"Average price change: {result['price_change_pct'].mean():.2f}%")
print(f"Products with price increase: {(result['price_change_pct'] > 0).sum()}")
print(f"Products with price decrease: {(result['price_change_pct'] < 0).sum()}")
print(f"Products unchanged: {(result['price_change_pct'] == 0).sum()}")

print("\nTop 5 price increases:")
print(result.nlargest(5, "price_change_pct")[["product_name", "current_price", "recommended_price", "price_change_pct"]])

print("\nTop 5 price decreases:")
print(result.nsmallest(5, "price_change_pct")[["product_name", "current_price", "recommended_price", "price_change_pct"]])
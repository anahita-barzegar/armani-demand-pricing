
"""
Transform module – cleaning, type casting, outlier handling.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Week",
    "Product",
    "Sales_Units",
    "Cost_of_Goods_Sold_COGS",
    "Inventory_Level",
    "Demand_Forecast",
    "Price_Per_Unit",
    "Gross_Profit",
    "Operating_Profit",
    "Revenue",
    "Inventory_Turnover_Ratio",
    "Gross_Profit_Margin",
    "Revenue_Growth",
]

NUMERIC_COLUMNS = [
    "Sales_Units",
    "Cost_of_Goods_Sold_COGS",
    "Inventory_Level",
    "Demand_Forecast",
    "Price_Per_Unit",
    "Gross_Profit",
    "Operating_Profit",
    "Revenue",
    "Inventory_Turnover_Ratio",
    "Gross_Profit_Margin",
    "Revenue_Growth",
]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline.
    """
    original_len = len(df)
    logger.info(f"Starting cleaning – original records: {original_len:,}")

    # 1. Standardize column names
    df.columns = df.columns.str.strip()

    # 2. Check required columns
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 3. Drop completely empty rows
    df = df.dropna(how="all")

    # 4. Type conversion
    df["Week"] = pd.to_numeric(df["Week"], errors="coerce").astype("Int64")
    df["Product"] = df["Product"].astype(str).str.strip()

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Drop rows with critical missing values
    df = df.dropna(subset=["Week", "Product", "Sales_Units", "Price_Per_Unit"])

    # 6. Fill missing values intelligently
    for col in ["Inventory_Level", "Demand_Forecast", "Cost_of_Goods_Sold_COGS"]:
        df[col] = df.groupby("Product")[col].transform(lambda x: x.fillna(x.median()))

    df["Gross_Profit_Margin"] = df["Gross_Profit_Margin"].fillna(0)
    df["Revenue_Growth"] = df["Revenue_Growth"].fillna(0)

    # 7. Remove illogical negative values
    df = df[df["Sales_Units"] >= 0]
    df = df[df["Inventory_Level"] >= 0]
    df = df[df["Price_Per_Unit"] > 0]

    # 8. Remove duplicates (Week + Product)
    before_dup = len(df)
    df = df.drop_duplicates(subset=["Week", "Product"], keep="first")
    logger.info(f"Removed {before_dup - len(df)} duplicate rows")

    # 9. Outlier treatment (IQR per product)
    def remove_outliers(group: pd.DataFrame) -> pd.DataFrame:
        for col in ["Sales_Units", "Revenue"]:
            Q1 = group[col].quantile(0.25)
            Q3 = group[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            group = group[(group[col] >= lower) & (group[col] <= upper)]
        return group

    df = df.groupby("Product", group_keys=False).apply(remove_outliers)

    # 10. Final sort
    df = df.sort_values(["Product", "Week"]).reset_index(drop=True)

    logger.info(f"Cleaning finished – remaining records: {len(df):,}")
    logger.info(f"Total removed: {original_len - len(df):,}")

    return df


def extract_category(product_name: str) -> str:
    """Simple category extraction from product name."""
    name = product_name.lower()
    if "rice" in name:
        return "Rice"
    if "oil" in name or "cooking" in name:
        return "Oil"
    if "sugar" in name:
        return "Sugar"
    if "milk" in name or "dairy" in name:
        return "Dairy"
    if "tea" in name:
        return "Tea"
    if "coffee" in name:
        return "Coffee"
    if "wheat" in name or "flour" in name:
        return "Wheat"
    return "Other"

"""
Load module – writes cleaned data into PostgreSQL Star Schema.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging
import numpy as np

from src.etl.transform import extract_category

logger = logging.getLogger(__name__)

DEFAULT_CONN = "postgresql+psycopg2://armani:armani123@localhost:5432/armani_trading"


def get_engine(connection_string: str = DEFAULT_CONN):
    return create_engine(connection_string)


def load_to_db(df: pd.DataFrame, connection_string: str = DEFAULT_CONN) -> None:
    """
    Load cleaned DataFrame into Star Schema tables.
    """
    engine = get_engine(connection_string)

    logger.info("Starting load into PostgreSQL...")

    with engine.begin() as conn:
        # 1. dim_product
        products = (
            df[["Product"]]
            .drop_duplicates()
            .rename(columns={"Product": "product_name"})
        )
        products["category"] = products["product_name"].apply(extract_category)

        conn.execute(text("TRUNCATE dim_product RESTART IDENTITY CASCADE"))
        products.to_sql("dim_product", conn, if_exists="append", index=False)
        logger.info(f"Loaded {len(products)} products into dim_product")

        # 2. dim_week
        weeks = df[["Week"]].drop_duplicates().rename(columns={"Week": "week_key"})
        weeks["year"] = 2020 + ((weeks["week_key"] - 1) // 52)
        weeks["week_of_year"] = ((weeks["week_key"] - 1) % 52) + 1
        weeks["year_week"] = weeks.apply(
            lambda r: f"{r['year']}-W{int(r['week_of_year']):02d}", axis=1
        )
        weeks["quarter"] = ((weeks["week_of_year"] - 1) // 13) + 1
        weeks["month"] = ((weeks["week_of_year"] - 1) // 4) + 1

        conn.execute(text("TRUNCATE dim_week CASCADE"))
        weeks.to_sql("dim_week", conn, if_exists="append", index=False)
        logger.info(f"Loaded {len(weeks)} weeks into dim_week")

        # 3. fact_weekly_sales
        product_map = pd.read_sql("SELECT product_id, product_name FROM dim_product", conn)
        df = df.merge(
            product_map,
            left_on="Product",
            right_on="product_name",
            how="left"
        )

        fact = df.rename(columns={
            "Week": "week_key",
            "Sales_Units": "sales_units",
            "Cost_of_Goods_Sold_COGS": "cogs",
            "Inventory_Level": "inventory_level",
            "Demand_Forecast": "demand_forecast",
            "Price_Per_Unit": "price_per_unit",
            "Gross_Profit": "gross_profit",
            "Operating_Profit": "operating_profit",
            "Revenue": "revenue",
            "Inventory_Turnover_Ratio": "inventory_turnover_ratio",
            "Gross_Profit_Margin": "gross_profit_margin",
            "Revenue_Growth": "revenue_growth",
        })

        fact_cols = [
            "week_key", "product_id",
            "sales_units", "cogs", "inventory_level", "demand_forecast",
            "price_per_unit", "gross_profit", "operating_profit", "revenue",
            "inventory_turnover_ratio", "gross_profit_margin", "revenue_growth"
        ]

        conn.execute(text("TRUNCATE fact_weekly_sales RESTART IDENTITY"))
        fact["revenue_growth"] = fact["revenue_growth"].replace(
            [np.inf, -np.inf],
            np.nan
        )
        fact[fact_cols].to_sql("fact_weekly_sales", conn, if_exists="append", index=False)
        logger.info(f"Loaded {len(fact)} rows into fact_weekly_sales")

    logger.info("Load completed successfully.")

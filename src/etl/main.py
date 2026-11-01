"""
ETL Pipeline entry point.
Usage:
    python -m src.etl.main
"""

import logging
import sys
from pathlib import Path

from src.etl.extract import extract_data
from src.etl.transform import clean_data
from src.etl.load import load_to_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("etl")


def run_etl():
    logger.info("=" * 60)
    logger.info("Starting ETL Pipeline – Armani Middle East Trading")
    logger.info("=" * 60)

    try:
        # Extract
        df_raw = extract_data()

        # Transform
        df_clean = clean_data(df_raw)

        # Save cleaned version
        processed_path = Path("data/processed/cleaned_sales.parquet")
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_parquet(processed_path, index=False)
        logger.info(f"Cleaned data saved to {processed_path}")

        # Load
        load_to_db(df_clean)

        logger.info("=" * 60)
        logger.info("ETL Pipeline finished successfully")
        logger.info("=" * 60)

    except Exception as e:
        logger.exception("ETL Pipeline failed")
        raise


if __name__ == "__main__":
    run_etl()

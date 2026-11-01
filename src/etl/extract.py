"""
Extract module – reads the raw Excel dataset.
"""

import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw/Sample_Data.xlsx")


def extract_data(file_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Read the source Excel file and return a DataFrame.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path}\n"
            "Please place Sample_Data.xlsx inside data/raw/"
        )

    logger.info(f"Reading data from {file_path}")
    df = pd.read_excel(file_path, engine="openpyxl")
    logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    return df

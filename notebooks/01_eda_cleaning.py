"""
01 - EDA & Data Cleaning
Armani Middle East Trading
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load raw data
df = pd.read_excel("data/raw/Sample_Data.xlsx")
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)

print("\nBasic statistics:")
print(df.describe())

# Distribution of Sales_Units
plt.figure(figsize=(10, 4))
sns.histplot(df["Sales_Units"].dropna(), bins=50)
plt.title("Distribution of Sales Units")
plt.show()

# Products
print("\nUnique products:", df["Product"].nunique())
print(df["Product"].value_counts())

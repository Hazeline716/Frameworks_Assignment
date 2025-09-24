import pandas as pd
import numpy as np

# --- 1. Load the dataset into a pandas DataFrame ---
print("--- Loading the metadata.csv file ---")
# The 'low_memory=False' argument is used to handle large files and prevent mixed data type warnings.
df = pd.read_csv('metadata.csv', low_memory=False)
print("Dataset loaded successfully!")


# --- 2. Examine the first few rows ---
print("\n--- First 5 rows of the DataFrame: ---")
print(df.head())


# --- 3. Basic data exploration ---
# Check the DataFrame dimensions (rows, columns)
print(f"\nDataFrame dimensions (rows, columns): {df.shape}")

# Identify data types of each column and check for non-null counts
print("\nDataFrame information (data types and non-null counts):")
df.info()


# --- 4. Check for missing values in each column ---
print("\n--- Missing values per column (Top 20): ---")
# This sorts the columns by the number of missing values in descending order
missing_values_count = df.isnull().sum().sort_values(ascending=False)
print(missing_values_count.head(20))


# --- 5. Generate basic statistics for numerical columns ---
print("\n--- Basic statistics for numerical columns: ---")
# The 'include=np.number' argument ensures only numerical columns are described
print(df.describe(include=np.number))

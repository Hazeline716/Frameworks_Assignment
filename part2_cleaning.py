import pandas as pd
import numpy as np

# --- 1. Load the raw dataset ---
print("--- Loading the raw metadata.csv file ---")
try:
    # Use low_memory=False to handle the large file without mixed data type warnings
    df = pd.read_csv('metadata.csv', low_memory=False)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: metadata.csv not found. Please make sure the file is in the same directory.")
    exit()

# --- 2. Handle missing data by dropping columns and filling values ---
print("\n--- Step 2: Handling Missing Values ---")

# These columns have a very high percentage of missing values and are not essential for our analysis.
# Dropping them simplifies the dataset.
columns_to_drop = [
    'sha', 'pmcid', 'pubmed_id', 'full_text_file', 's2_id', 'source_x'
]
df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

# Fill missing values in key text columns with an empty string ('')
# This prevents errors in later text-based analysis, like word counts.
df_cleaned['abstract'] = df_cleaned['abstract'].fillna('')
df_cleaned['title'] = df_cleaned['title'].fillna('')

print("Dropped unnecessary columns and filled missing values in 'abstract' and 'title'.")
print(f"New DataFrame dimensions: {df_cleaned.shape}")

# --- 3. Prepare data for analysis ---
print("\n--- Step 3: Preparing Data for Analysis ---")

# Convert the 'publish_time' column to a proper datetime format.
# The 'errors=coerce' argument will turn any unparseable dates into 'NaT' (Not a Time).
df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')

# Drop any rows where the 'publish_time' was unparseable.
df_cleaned.dropna(subset=['publish_time'], inplace=True)

# Create a new 'year' column.
# This makes it easy to analyze publication trends over time.
df_cleaned['year'] = df_cleaned['publish_time'].dt.year.astype(int)

# Create a new 'abstract_word_count' column.
df_cleaned['abstract_word_count'] = df_cleaned['abstract'].apply(lambda x: len(x.split()))

print("Converted 'publish_time' to datetime and created 'year' and 'abstract_word_count' columns.")
print("\nCleaned and prepared DataFrame info:")
df_cleaned.info()

# Save the cleaned DataFrame to a new CSV file.
# This allows you to use this cleaned data directly in the next step (analysis),
# without having to re-run the cleaning process every time.
df_cleaned.to_csv('cleaned_metadata.csv', index=False)
print("\nCleaned data saved to 'cleaned_metadata.csv'.")

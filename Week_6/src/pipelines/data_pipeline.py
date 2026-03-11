import os
import pandas as pd

# PATHS

RAW_DATA_PATH = "src/data/raw/diabetes.csv"

PROCESSED_DATA_PATH = "src/data/processed/diabetes_clean.csv"

LOG_DIR = "src/logs"

os.makedirs("src/data/processed", exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# 1. LOAD DATA

def load_data():

    df = pd.read_csv(RAW_DATA_PATH)

    print("\nDataset Loaded Successfully")
    print(f"Dataset Shape: {df.shape}")

    return df


# 2. CLEAN DATA

def clean_data(df):

    df = df.copy()

    # Handle missing values (Adult dataset often uses '?' as missing)

    # Handle missing values

    df.replace("?", pd.NA, inplace=True)

# Numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

# Categorical columns
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns


# Fill numeric with median
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())


# Fill categorical with mode
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Remove duplicates
        df.drop_duplicates(inplace=True)

    # Remove outliers using IQR for numeric columns

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    numeric_cols = [col for col in numeric_cols if col != "income"]

    for col in numeric_cols:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        before = df.shape[0]

        df = df[(df[col] >= lower) & (df[col] <= upper)]

        after = df.shape[0]

        print(f"{col}: removed {before - after} outliers")

    print(f"Cleaned Dataset Shape: {df.shape}")

    return df


# 3. SAVE PROCESSED DATA

def save_processed_data(df):

    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("\nProcessed file saved:")
    print(PROCESSED_DATA_PATH)


# 4. PRINT DATASET SUMMARY

def print_dataset_summary(df):

    print("\nDataset Info")
    print(df.info())

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nStatistical Summary")
    print(df.describe())


# 5. EXECUTE PIPELINE

def main():

    df = load_data()

    df = clean_data(df)

    save_processed_data(df)

    print_dataset_summary(df)

    print("\nPipeline completed successfully")


if __name__ == "__main__":
    main()
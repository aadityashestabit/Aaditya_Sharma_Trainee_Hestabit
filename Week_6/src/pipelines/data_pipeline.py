import os
import pandas as pd
import numpy as np

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

# clean data
def clean_data(df):
    df = df.copy()

    cols_with_zero_invalid = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

    # Step 1: Replace invalid zeros
    df[cols_with_zero_invalid] = df[cols_with_zero_invalid].replace(0, np.nan)

    # add missing indicator
    for col in cols_with_zero_invalid:
        df[f"{col}_missing"] = df[col].isna().astype(int)

    # Step 2: Median imputation - filling missing values
    for col in cols_with_zero_invalid:
        df[col] = df[col].fillna(df[col].median())

    # Step 3: Remove duplicates
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    print(f"Removed {before - df.shape[0]} duplicate rows")

    # Step 4: Outlier clipping (exclude target)
    numeric_cols = [col for col in df.select_dtypes(include=["int64", "float64"]).columns 
                    if col != "Outcome"]

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = df[col].clip(lower, upper)

    # Step 5: Validation
    print("\nPost-clean validation:")
    print("Missing values:\n", df.isnull().sum())

    print("\nZero values (should be 0):")
    for col in cols_with_zero_invalid:
        print(col, (df[col] == 0).sum())

    print(f"\nCleaned Dataset Shape: {df.shape}")

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
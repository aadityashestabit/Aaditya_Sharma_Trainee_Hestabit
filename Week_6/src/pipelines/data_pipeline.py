import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno



# PATHS


RAW_TRAIN_PATH = "src/data/raw/train.csv"
RAW_TEST_PATH = "src/data/raw/test.csv"


PROCESSED_TRAIN_PATH = "src/data/processed/train_clean.csv"
PROCESSED_TEST_PATH = "src/data/processed/test_clean.csv"

LOG_DIR = "src/logs"

os.makedirs("src/data/processed", exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)



# 1. LOAD DATA

def load_data():
    train = pd.read_csv(RAW_TRAIN_PATH)
    test = pd.read_csv(RAW_TEST_PATH)


    print("\nDataset Loaded Successfully")
    print(f"Train Shape: {train.shape}")
    print(f"Test Shape: {test.shape}")

    return train, test



# 2. CLEAN DATA

def clean_data(df, is_train=True):

    df = df.copy()

    # Removinr unnecessary columns

    df.drop(columns=["Cabin", "Ticket", "Name"], errors="ignore", inplace=True)

    # Filling missing values

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    # Removing duplicates

    df.drop_duplicates(inplace=True)

    # Removing outliers using IQR only from traning data
    # Removing outliers using IQR only from training data
    if is_train:

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        numeric_cols = [col for col in numeric_cols if col not in ["PassengerId", "Survived"]]

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

        
            print(f"Cleaned Train Shape: {df.shape}")

    return df



# Saving processed data 


def save_processed_data(train_df, test_df):

    train_df.to_csv(PROCESSED_TRAIN_PATH, index=False)
    test_df.to_csv(PROCESSED_TEST_PATH, index=False)

    print("Processed files saved:")
    print(PROCESSED_TRAIN_PATH)
    print(PROCESSED_TEST_PATH)


# Printing dataset summary 

def print_dataset_summary(df):
    """Print useful dataset statistics"""

    print("\nDataset Info")
    print(df.info())

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nStatistical Summary")
    print(df.describe())



# Executing Pipeline


def main():

    train, test = load_data()

    train = clean_data(train, True)
    test = clean_data(test, False)

    save_processed_data(train, test)
    print_dataset_summary(train)

    print("Pipeline completed successfully")


main()
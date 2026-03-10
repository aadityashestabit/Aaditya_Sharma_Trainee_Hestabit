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
    if is_train:

        Q1 = df["Fare"].quantile(0.25)
        Q3 = df["Fare"].quantile(0.75)
        IQR = Q3 - Q1

        df = df[
            (df["Fare"] >= Q1 - 3 * IQR) &
            (df["Fare"] <= Q3 + 3 * IQR)
        ]

        print(f"Outliers removed from Fare:")

        print(f"Cleaned {'Train' if is_train else 'Test'} Shape: {df.shape}")

    return df



# Saving processed data 


def save_processed_data(train_df, test_df):

    train_df.to_csv(PROCESSED_TRAIN_PATH, index=False)
    test_df.to_csv(PROCESSED_TEST_PATH, index=False)

    print("Processed files saved:")
    print(PROCESSED_TRAIN_PATH)
    print(PROCESSED_TEST_PATH)



# 3. Charts formation using EDA


def perform_eda(df):

    print("Generating EDA charts...")

    # Missing values heatmap
    plt.figure(figsize=(8,4))
    msno.heatmap(df)
    plt.title("Missing Values Heatmap")
    plt.show()
    plt.savefig(f"{LOG_DIR}/missing_values_heatmap.png")
    plt.close()

    # Correlation matrix
    
    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(8,5))

    if corr.shape[0] > 1:
        sns.heatmap(corr, annot=True, cmap="coolwarm")
    else:
        print("Not enough numeric features for correlation heatmap")

    plt.title("Correlation Matrix")
    plt.show() #this show the chart flrmed
    plt.savefig(f"{LOG_DIR}/correlation_matrix.png")
    plt.close()

    # Target distribution

    plt.figure(figsize=(5,4))
    df["Survived"].value_counts().plot(kind="bar")
    plt.title("Target Distribution")
    plt.show()
    plt.xlabel("Survived")
    plt.ylabel("Count")
    plt.savefig(f"{LOG_DIR}/target_distribution.png")
    plt.close()

    # Feature distributions

    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols].hist(figsize=(10,8), bins=20)

    plt.suptitle("Feature Distributions")
    plt.show()
    plt.savefig(f"{LOG_DIR}/feature_distributions.png")
    plt.close()

    print(f"EDA charts saved to {LOG_DIR}")


# Printing dataset summary 

def print_dataset_summary(df):
    """Print useful dataset statistics"""

    print("\nDataset Info")
    print(df.info())

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nStatistical Summary")
    print(df.describe())



# 4. Executing Pipeline


def main():

    train, test = load_data()

    train = clean_data(train, True)
    test = clean_data(test, False)

    save_processed_data(train, test)
    print_dataset_summary(train)
    perform_eda(train)

    print("Pipeline completed successfully")


main()
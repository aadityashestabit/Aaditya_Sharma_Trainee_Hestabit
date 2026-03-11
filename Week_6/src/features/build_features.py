import os
import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

DATA_PATH = "src/data/processed/train_clean.csv"
FEATURE_LIST_PATH = "src/features/feature_list.json"


def load_data():
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded:", df.shape)
    return df


def create_new_features(df):

    #  Family Size
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

    #  Is Alone
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    # Fare per person
    df["Fare_per_person"] = df["Fare"] / df["FamilySize"]

    # Age Group
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
    )

    #  Is Child
    df["IsChild"] = (df["Age"] < 12).astype(int)

    # Fare Category
    df["FareCategory"] = pd.cut(
        df["Fare"],
        bins=[0, 10, 30, 100, 600],
        labels=["Low", "Medium", "High", "VeryHigh"]
    )

    # Has Parents
    df["HasParents"] = (df["Parch"] > 0).astype(int)

    # Has Siblings
    df["HasSiblings"] = (df["SibSp"] > 0).astype(int)

    # Fare adjusted by class
    df["PclassFare"] = df["Fare"] / df["Pclass"]

    # Family Type
    df["FamilyType"] = pd.cut(
        df["FamilySize"],
        bins=[0,1,4,10],
        labels=["Alone","SmallFamily","LargeFamily"]
    )

    return df


def encode_features(df):

    categorical_cols = [
    "Sex",
    "Embarked",
    "AgeGroup",
    "FareCategory",
    "FamilyType"
    ]

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df


def scale_features(df):

    scaler = StandardScaler()

    numeric_cols = ["Age", "Fare", "FamilySize", "Fare_per_person"]

    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df


def split_dataset(df):

    X = df.drop(columns=["Survived"])
    y = df["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    return X_train, X_test, y_train, y_test


def save_feature_list(columns):

    with open(FEATURE_LIST_PATH, "w") as f:
        json.dump(list(columns), f, indent=4)

    print("Feature list saved")


def main():

    df = load_data()

    df = create_new_features(df)

    df = encode_features(df)

    df = scale_features(df)

    X_train, X_test, y_train, y_test = split_dataset(df)

    save_feature_list(X_train.columns)

    print("Feature pipeline completed")


if __name__ == "__main__":
    main()
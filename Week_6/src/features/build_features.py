import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Paths
DATA_PATH = "src/data/processed/diabetes_clean.csv"
FEATURE_LIST_PATH = "src/features/feature_list.json"
FEATURE_DATA_DIR = "src/data/features"

os.makedirs(FEATURE_DATA_DIR, exist_ok=True)


# Save split datasets
def save_feature_datasets(X_train, X_test, y_train, y_test):

    X_train.to_csv(f"{FEATURE_DATA_DIR}/X_train.csv", index=False)
    X_test.to_csv(f"{FEATURE_DATA_DIR}/X_test.csv", index=False)

    y_train.to_csv(f"{FEATURE_DATA_DIR}/y_train.csv", index=False)
    y_test.to_csv(f"{FEATURE_DATA_DIR}/y_test.csv", index=False)

    print("Feature datasets saved")


# 1 Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print("Shape:", df.shape)


# 2 Create new features

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0,30,45,60,100],
    labels=["Young","Adult","MiddleAge","Senior"]
)

df["BMICategory"] = pd.cut(
    df["BMI"],
    bins=[0,18.5,25,30,100],
    labels=["Underweight","Normal","Overweight","Obese"]
)

df["HighGlucose"] = (df["Glucose"] > 140).astype(int)

df["HighBP"] = (df["BloodPressure"] > 90).astype(int)

df["BMI_Age"] = df["BMI"] * df["Age"]

df["Insulin_Glucose_Ratio"] = df["Insulin"] / (df["Glucose"] + 1)

df["MultiplePregnancies"] = (df["Pregnancies"] >= 3).astype(int)

df["Skin_BMI_Ratio"] = df["SkinThickness"] / (df["BMI"] + 1)

df["Glucose_BMI"] = df["Glucose"] * df["BMI"]

df["Age_Glucose"] = df["Age"] * df["Glucose"]

print("New features created")


# 3 Encode categorical columns

df = pd.get_dummies(df, columns=["AgeGroup","BMICategory"], drop_first=True)

print("Categorical features encoded")


# 4 Scale numeric columns

scaler = StandardScaler()

numeric_cols = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print("Numeric features scaled")


# Save dataset with features
FEATURE_DATA_PATH = "src/data/processed/diabetes_features.csv"

df.to_csv(FEATURE_DATA_PATH, index=False)

print("Feature dataset saved:", FEATURE_DATA_PATH)


# 5 Split dataset

X = df.drop(columns=["Outcome"])
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


# Save split datasets
save_feature_datasets(X_train, X_test, y_train, y_test)


# 6 Save feature list

feature_list = list(X_train.columns)

with open(FEATURE_LIST_PATH, "w") as f:
    json.dump(feature_list, f, indent=4)

print("Feature list saved")


print("Feature pipeline completed")
import pandas as pd
import json
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_classif

# Paths
DATA_PATH = "src/data/processed/diabetes_clean.csv"
FEATURE_LIST_PATH = "src/features/feature_list.json"
SELECTED_FEATURES_PATH = "src/features/selected_features.json"
FEATURE_DATA_DIR = "src/data/features"

os.makedirs(FEATURE_DATA_DIR, exist_ok=True)


# Save datasets
def save_feature_datasets(X_train, X_test, y_train, y_test):
    X_train.to_csv(f"{FEATURE_DATA_DIR}/X_train.csv", index=False)
    X_test.to_csv(f"{FEATURE_DATA_DIR}/X_test.csv", index=False)
    y_train.to_csv(f"{FEATURE_DATA_DIR}/y_train.csv", index=False)
    y_test.to_csv(f"{FEATURE_DATA_DIR}/y_test.csv", index=False)
    print("Feature datasets saved")


# ===============================
# 1. LOAD DATA
# ===============================
df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print("Shape:", df.shape)


# ===============================
# 2. FEATURE ENGINEERING
# ===============================

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["Young", "Adult", "MiddleAge", "Senior"]
)

df["BMICategory"] = pd.cut(
    df["BMI"],
    bins=[0, 18.5, 25, 30, 100],
    labels=["Underweight", "Normal", "Overweight", "Obese"]
)

df["HighGlucose"] = (df["Glucose"] > 140).astype(int)
df["HighBP"] = (df["BloodPressure"] > 90).astype(int)
df["BMI_Age"] = df["BMI"] * df["Age"]
df["Insulin_Glucose_Ratio"] = df["Insulin"] / (df["Glucose"] + 1)
df["MultiplePregnancies"] = (df["Pregnancies"] >= 3).astype(int)
df["Skin_BMI_Ratio"] = df["SkinThickness"] / (df["BMI"] + 1)
df["Glucose_BMI"] = df["Glucose"] * df["BMI"]
df["Age_Glucose"] = df["Age"] * df["Glucose"]


print("Age skew :",df["Age"].skew)

# Log transform
df["DPF_log"] = np.log1p(df["DiabetesPedigreeFunction"])
df["Age_log"] = np.log1p(df["Age"])

df.drop(columns=["DiabetesPedigreeFunction", "Age"], inplace=True)

print("New features created")


# ===============================
# 3. ENCODING
# ===============================

df = pd.get_dummies(df, columns=["AgeGroup", "BMICategory"], drop_first=True)

bool_cols = df.select_dtypes(include="bool").columns
df[bool_cols] = df[bool_cols].astype(int)

print("Categorical features encoded")


# ===============================
# 4. SPLIT DATA (IMPORTANT FIRST)
# ===============================

X = df.drop(columns=["Outcome"])
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


# ===============================
# 5. SCALING (NO LEAKAGE)
# ===============================

scaler = StandardScaler()

categorical_cols = [col for col in X_train.columns if "Category" in col or "AgeGroup" in col]
numeric_cols = [col for col in X_train.columns if col not in categorical_cols]

X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

print("Scaling applied")


# ===============================
# 6. FEATURE SELECTION (TOP 13)
# ===============================

mi = mutual_info_classif(X_train, y_train)

mi_scores = pd.Series(mi, index=X_train.columns).sort_values(ascending=False)

print("\nFeature Importance Scores:")
print(mi_scores)

TOP_K = 13
selected_features = mi_scores.head(TOP_K).index

print("\nSelected Features:")
print(selected_features)

# Apply selection
X_train = X_train[selected_features]
X_test = X_test[selected_features]


# ===============================
# 7. SAVE OUTPUTS
# ===============================

save_feature_datasets(X_train, X_test, y_train, y_test)

# Save feature list
with open(FEATURE_LIST_PATH, "w") as f:
    json.dump(list(X_train.columns), f, indent=4)

# Save selected features
with open(SELECTED_FEATURES_PATH, "w") as f:
    json.dump(list(selected_features), f, indent=4)

print("Feature list + selected features saved")


print("\n✅ PIPELINE COMPLETED SUCCESSFULLY")
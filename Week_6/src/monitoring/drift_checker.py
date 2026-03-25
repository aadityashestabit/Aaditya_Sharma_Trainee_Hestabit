import pandas as pd

TRAIN_DATA = "src/data/processed/diabetes_clean.csv"
LOG_DATA = "src/prediction_logs.csv"

# Load data
train = pd.read_csv(TRAIN_DATA)
logs = pd.read_csv(LOG_DATA)

# Drop non-feature columns
train = train.drop(columns=["Outcome"], errors="ignore")
logs = logs.drop(columns=["request_id", "timestamp", "prediction"], errors="ignore")

# Ensure same columns
common_cols = train.columns.intersection(logs.columns)

train = train[common_cols]
logs = logs[common_cols]

print("\n=== Drift Check ===")

for col in common_cols:
    train_mean = train[col].mean()
    log_mean = logs[col].mean()

    diff = abs(train_mean - log_mean)

    print(f"\nFeature: {col}")
    print(f"Train Mean: {train_mean:.2f}")
    print(f"Prod Mean:  {log_mean:.2f}")
    print(f"Difference: {diff:.2f}")

    # Simple drift flag
    if diff > 10:   # threshold (tune this)
        print("⚠️ Drift Detected")
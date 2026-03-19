import pandas as pd

TRAIN_DATA = "src/data/features/X_train.csv"
LOG_DATA = "src/logs/prediction_logs.csv"


train = pd.read_csv(TRAIN_DATA)

try:
    logs = pd.read_csv(LOG_DATA)
except:
    print("No predictions yet")
    exit()

print("Train stats")
print(train.describe())

print("\nPrediction stats")
print(logs.describe())
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.feature_selection import mutual_info_classif

DATA_PATH = "src/data/processed/diabetes_features.csv"
LOG_DIR   = "src/logs"

os.makedirs(LOG_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)
    X  = df.drop(columns=["Outcome"])
    y  = df["Outcome"]
    return X, y


def compute_mi_scores(X, y):
    if X is None or y is None:
        raise ValueError("Input data cannot be None")

    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame")

    if len(X) > 100000:  # limit size
        raise ValueError("Dataset too large")

    mi = mutual_info_classif(X, y)
    mi_scores = pd.Series(mi, index=X.columns).sort_values(ascending=False)

    return mi_scores

def plot_feature_importance(scores):
    plt.figure(figsize=(10, 5))
    scores.plot(kind="bar")
    plt.title("Feature Importance (Mutual Information)")
    plt.ylabel("Score")                      # moved BEFORE savefig
    plt.xticks(rotation=45, ha="right")      # ha="right" aligns labels cleanly
    plt.tight_layout()
    plt.savefig(f"{LOG_DIR}/feature_importance.png")
    plt.show()
    print(f"Plot saved to {LOG_DIR}/feature_importance.png")


def main():
    X, y    = load_data()
    scores  = compute_mi_scores(X, y)

    print("\nFeature Importance Scores:")
    print(scores)

    plot_feature_importance(scores)


if __name__ == "__main__":
    main()
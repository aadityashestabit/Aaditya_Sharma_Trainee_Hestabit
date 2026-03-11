import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

DATA_PATH = "src/data/processed/diabetes_features.csv"
LOG_DIR = "src/logs"


def load_data():

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    return X, y


def mutual_information_selection(X, y):

    mi = mutual_info_classif(X, y)

    mi_scores = pd.Series(mi, index=X.columns)

    mi_scores = mi_scores.sort_values(ascending=False)

    print("\nFeature Importance Scores:")
    print(mi_scores)

    return mi_scores


def plot_feature_importance(scores):

    plt.figure(figsize=(10,5))

    scores.plot(kind="bar")

    plt.title("Feature Importance (Mutual Information)")
    plt.savefig(f"{LOG_DIR}/feature selector.png")

    plt.ylabel("Score")

    plt.xticks(rotation=45)

    plt.show()


def main():

    X, y = load_data()

    scores = mutual_information_selection(X, y)

    plot_feature_importance(scores)


if __name__ == "__main__":
    main()
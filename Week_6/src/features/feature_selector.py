import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

DATA_PATH = "src/data/processed/train_clean.csv"


def load_data():

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["Survived"])
    y = df["Survived"]

    return X, y


def mutual_information_selection(X, y):

    mi = mutual_info_classif(X, y)

    mi_scores = pd.Series(mi, index=X.columns)

    mi_scores = mi_scores.sort_values(ascending=False)

    print(mi_scores)

    return mi_scores


def plot_feature_importance(scores):

    scores.plot(kind="bar")

    plt.title("Feature Importance (Mutual Information)")

    plt.show()


def main():

    X, y = load_data()

    scores = mutual_information_selection(X, y)

    plot_feature_importance(scores)


if __name__ == "__main__":
    main()
import pandas as pd
import json
import joblib
import os

from sklearn.pipeline import Pipeline
from src.pipelines.transformers import FeatureEngineer
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import xgboost as xgb
import matplotlib.pyplot as plt


# Paths
DATA_PATH = "src/data/processed/diabetes_clean.csv" 
MODEL_PATH = "src/models/best_model.pkl"
METRICS_PATH = "src/evaluation/metrics.json"
CM_PATH = "src/evaluation/confusion_matrix.png"


# Load data
def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]
    return X, y


# Check target imbalance
def check_class_imbalance(y):
    distribution = pd.Series(y).value_counts(normalize=True)

    print("\nClass Distribution:")
    print(distribution)

    imbalance_ratio = distribution.min() / distribution.max()

    if imbalance_ratio < 0.5:
        print("Imbalanced dataset detected")
        return True, distribution
    else:
        print("Dataset is balanced")
        return False, distribution


# Define models
def get_models(y_train):

    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    def make_pipeline(model):
        return Pipeline([
            ("feature_engineering", FeatureEngineer()),
            ("scaler", StandardScaler()),
            ("model", model)
        ])

    models = {
        "Logistic Regression": make_pipeline(
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
        ),
        "Random Forest": make_pipeline(
            RandomForestClassifier(class_weight="balanced", random_state=42)
        ),
        "XGBoost": make_pipeline(
            xgb.XGBClassifier(
                use_label_encoder=False,
                eval_metric='logloss',
                scale_pos_weight=scale_pos_weight,
                random_state=42
            )
        ),
        "Neural Network": make_pipeline(
            MLPClassifier(max_iter=500, random_state=42)
        )
    }

    return models


# Evaluate model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }

    return metrics, y_pred


# Main pipeline
def train_pipeline():

    # Load data
    X, y = load_data()

    # Split data (MISSING EARLIER ❌)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Check imbalance
    is_imbalanced, distribution = check_class_imbalance(y_train)

    # Models
    models = get_models(y_train)

    results = {}
    best_model = None
    best_score = 0
    best_name = ""

    for name, model in models.items():
        print(f"\nTraining {name}...")

        # Cross-validation
        cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='f1').mean()

        # Train
        model.fit(X_train, y_train)

        # Evaluate
        metrics, y_pred = evaluate_model(model, X_test, y_test)

        metrics["cv_f1"] = cv_score
        results[name] = metrics

        print(f"{name} CV F1: {cv_score}")

        # Combined score
        score = (metrics["f1_score"] + cv_score) / 2

        if score > best_score:
            best_score = score
            best_model = model
            best_name = name

    # Save best model
    os.makedirs("src/models", exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    # Save metrics
    os.makedirs("src/evaluation", exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    # Confusion matrix
    y_pred = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()

    plt.savefig(CM_PATH)

    print(f"\nBest Model: {best_name}")
    print(f" Model saved at: {MODEL_PATH}")
    print(f" Metrics saved at: {METRICS_PATH}")


if __name__ == "__main__":
    train_pipeline()
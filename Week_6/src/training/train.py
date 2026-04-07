import pandas as pd
import json
import joblib
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from src.pipelines.transformers import FeatureEngineer
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import cross_val_score, train_test_split

# import evaluation metrics
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay
)

# Models import 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb



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
            ("feature_selection", SelectKBest(score_func=mutual_info_classif, k=12)),
            ("model", model)
        ])

    models = {
        "Logistic Regression": make_pipeline(
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
        ),
        "Random Forest": make_pipeline(
            RandomForestClassifier(class_weight="balanced",
                                   random_state=42,
                                   max_depth=6,
                                   min_samples_leaf=5,
                                   min_samples_split=10,
                                   max_features="sqrt",
                                   n_estimators=200,
                                   max_samples=0.8
                                   )
        ),
        "XGBoost": make_pipeline(
            xgb.XGBClassifier(
                use_label_encoder=False,
                eval_metric='logloss',
                scale_pos_weight=scale_pos_weight,
                random_state=42,
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
            )
        ),
        "Neural Network": make_pipeline(
            MLPClassifier(max_iter=500, random_state=42,hidden_layer_sizes=(64, 32),
            early_stopping=True)
        )
    }

    return models



# Evaluate model
def evaluate_model(model, X_test, y_test):
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }

    return metrics, y_pred

def plot_bias_variance(model, X_train, y_train, model_name="Model"):
    
    train_sizes, train_scores, val_scores = learning_curve(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="f1",
        train_sizes=np.linspace(0.1, 1.0, 10),
        n_jobs=-1
    )

    # Mean and std across folds
    train_mean = train_scores.mean(axis=1)
    train_std  = train_scores.std(axis=1)
    val_mean   = val_scores.mean(axis=1)
    val_std    = val_scores.std(axis=1)

    plt.figure(figsize=(8, 5))

    # Train line
    plt.plot(train_sizes, train_mean, color="#185FA5", label="Training score", linewidth=2)
    plt.fill_between(train_sizes,
                     train_mean - train_std,
                     train_mean + train_std,
                     alpha=0.15, color="#185FA5")

    # Validation line
    plt.plot(train_sizes, val_mean, color="#D85A30", label="Validation score", linewidth=2)
    plt.fill_between(train_sizes,
                     val_mean - val_std,
                     val_mean + val_std,
                     alpha=0.15, color="#D85A30")

    plt.xlabel("Training set size")
    plt.ylabel("F1 Score")
    plt.title(f"Learning curve — {model_name}")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"src/evaluation/learning_curve_{model_name}.png")
    plt.show()
    plt.close()
    
    
# Main pipeline
def train_pipeline():

    # Load data
    X, y = load_data()

    # Split data
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
        score = cv_score
        if score > best_score:
            best_score = score
            best_model = model
            best_name = name
            


    # Save best model
    os.makedirs("src/models", exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        plot_bias_variance(model, X_train, y_train, model_name=name)
    

# PRINT SELECTED FEATURES


    selector = best_model.named_steps["feature_selection"]
    feature_engineer = best_model.named_steps["feature_engineering"]

    feature_names = feature_engineer.get_feature_names_out()
    selected_indices = selector.get_support(indices=True)

    selected_features = [feature_names[i] for i in selected_indices]

    print("\nSelected Features (Top 12):")
    for f in selected_features:
        print(f)

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
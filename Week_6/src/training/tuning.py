import pandas as pd
import json
import optuna
import joblib

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.pipelines.transformers import FeatureEngineer



# PATHS

DATA_PATH = "src/data/processed/diabetes_clean.csv"
RESULTS_PATH = "src/tuning/tuning_results.json"
MODEL_PATH = "src/models/tuned_model.pkl"



# LOAD DATA (RAW)

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["Outcome"])
y = df["Outcome"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



# OPTUNA OBJECTIVE (PIPELINE)

def objective(trial):

    solver = trial.suggest_categorical("solver", ["lbfgs", "liblinear", "saga"])

    if solver == "lbfgs":
        penalty = "l2"
    else:
        penalty = trial.suggest_categorical("penalty", ["l1", "l2"])

    params = {
        "C": trial.suggest_float("C", 0.01, 10.0, log=True),
        "penalty": penalty,
        "solver": solver,
        "max_iter": 5000,
        "class_weight": trial.suggest_categorical("class_weight", ["balanced", None]),
    }

    pipeline = Pipeline([
        ("feature_engineering", FeatureEngineer()),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(**params))
    ])

    score = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="roc_auc").mean()
    return score



# RUN OPTUNA

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

best_params = study.best_params
best_cv_score = study.best_value

print("\nBest Params:", best_params)
print("Best CV ROC-AUC:", best_cv_score)


# TRAIN FINAL PIPELINE MODEL

best_model = Pipeline([
    ("feature_engineering", FeatureEngineer()),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(**best_params, max_iter=5000))
])

best_model.fit(X_train, y_train)
print("Final tuned pipeline trained")



# TEST EVALUATION

test_preds = best_model.predict(X_test)
test_probs = best_model.predict_proba(X_test)[:, 1]

test_metrics = {
    "accuracy": accuracy_score(y_test, test_preds),
    "precision": precision_score(y_test, test_preds),
    "recall": recall_score(y_test, test_preds),
    "f1": f1_score(y_test, test_preds),
    "roc_auc": roc_auc_score(y_test, test_probs),
}

print(f"\nCV ROC-AUC:   {best_cv_score:.4f}")
print(f"Test ROC-AUC: {test_metrics['roc_auc']:.4f}")
print(f"Gap:          {best_cv_score - test_metrics['roc_auc']:.4f}")
print("Test Metrics:", test_metrics)


# SAVE MODEL + RESULTS
import os
os.makedirs("src/models", exist_ok=True)
os.makedirs("src/tuning", exist_ok=True)

joblib.dump(best_model, MODEL_PATH)
print("Tuned model saved:", MODEL_PATH)

output = {
    "model": "LogisticRegression",
    "best_params": best_params,
    "cv_roc_auc": best_cv_score,
    "test_metrics": test_metrics,
}

with open(RESULTS_PATH, "w") as f:
    json.dump(output, f, indent=4)

print("Tuning results saved:", RESULTS_PATH)
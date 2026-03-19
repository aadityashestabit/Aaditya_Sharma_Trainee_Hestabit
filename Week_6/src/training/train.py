import pandas as pd
import json
import joblib
import optuna

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression


# Paths
X_TRAIN_PATH = "src/data/features/X_train.csv"
Y_TRAIN_PATH = "src/data/features/y_train.csv"
X_TEST_PATH = "src/data/features/X_test.csv"
Y_TEST_PATH = "src/data/features/y_test.csv"

MODEL_PATH = "src/models/tuned_model.pkl"
RESULTS_PATH = "src/tuning/tuning_results.json"


# Load data
X_train = pd.read_csv(X_TRAIN_PATH)
y_train = pd.read_csv(Y_TRAIN_PATH).squeeze()

X_test = pd.read_csv(X_TEST_PATH)
y_test = pd.read_csv(Y_TEST_PATH).squeeze()


# ===============================
# OPTUNA OBJECTIVE
# ===============================
def objective(trial):

    params = {
        "C": trial.suggest_float("C", 0.01, 10.0, log=True),
        "penalty": "l2",
        "solver": "lbfgs",
        "max_iter": 5000,
        "class_weight": "balanced"
    }

    model = LogisticRegression(**params)

    score = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="roc_auc"
    ).mean()

    return score


# ===============================
# RUN TUNING
# ===============================
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

best_params = study.best_params
best_cv_score = study.best_value

print("Best Params:", best_params)
print("Best CV ROC-AUC:", best_cv_score)


# ===============================
# TRAIN FINAL MODEL
# ===============================
model = LogisticRegression(
    **best_params,
    penalty="l2",
    solver="lbfgs",
    max_iter=5000,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ===============================
# TEST EVALUATION
# ===============================
test_preds = model.predict(X_test)
test_probs = model.predict_proba(X_test)[:, 1]

test_metrics = {
    "accuracy": accuracy_score(y_test, test_preds),
    "precision": precision_score(y_test, test_preds),
    "recall": recall_score(y_test, test_preds),
    "f1": f1_score(y_test, test_preds),
    "roc_auc": roc_auc_score(y_test, test_probs)
}

print("Test Metrics:", test_metrics)


# ===============================
# SAVE MODEL + RESULTS
# ===============================
joblib.dump(model, MODEL_PATH)

with open(RESULTS_PATH, "w") as f:
    json.dump({
        "model": "LogisticRegression",
        "best_params": best_params,
        "cv_roc_auc": best_cv_score,
        "test_metrics": test_metrics
    }, f, indent=4)

print("Tuned model and results saved")
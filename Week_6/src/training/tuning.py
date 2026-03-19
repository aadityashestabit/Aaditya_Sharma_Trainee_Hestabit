import pandas as pd
import json
import optuna
import joblib

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression

# Paths
X_TRAIN_PATH = "src/data/features/X_train.csv"
Y_TRAIN_PATH = "src/data/features/y_train.csv"
X_TEST_PATH  = "src/data/features/X_test.csv"
Y_TEST_PATH  = "src/data/features/y_test.csv"
RESULTS_PATH = "src/tuning/tuning_results.json"
MODEL_PATH   = "src/models/tuned_model.pkl"

X_train = pd.read_csv(X_TRAIN_PATH)
y_train = pd.read_csv(Y_TRAIN_PATH).squeeze()
X_test  = pd.read_csv(X_TEST_PATH)
y_test  = pd.read_csv(Y_TEST_PATH).squeeze()


# ===============================
# 1. OPTUNA OBJECTIVE  ← CHANGED
# ===============================
def objective(trial):
    solver = trial.suggest_categorical("solver", ["lbfgs", "liblinear", "saga"])

    # l1 only works with liblinear / saga; lbfgs only supports l2
    if solver == "lbfgs":
        penalty = "l2"
    else:
        penalty = trial.suggest_categorical("penalty", ["l1", "l2"])

    params = {
        "C":            trial.suggest_float("C", 0.01, 10.0, log=True),
        "penalty":      penalty,
        "solver":       solver,
        "max_iter":     5000,
        # ← was hardcoded "balanced"; now tuned
        "class_weight": trial.suggest_categorical("class_weight", ["balanced", None]),
    }

    model = LogisticRegression(**params)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc").mean()
    return score


# ===============================
# 2. RUN OPTUNA
# ===============================
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

best_params  = study.best_params
best_cv_score = study.best_value

print("Best Params:", best_params)
print("Best CV ROC-AUC:", best_cv_score)


# ===============================
# 3. TRAIN FINAL MODEL
# ===============================
best_model = LogisticRegression(**best_params, max_iter=5000)
best_model.fit(X_train, y_train)
print("Final tuned model trained")


# ===============================
# 4. TEST EVALUATION
# ===============================
test_preds = best_model.predict(X_test)
test_probs = best_model.predict_proba(X_test)[:, 1]

test_metrics = {
    "accuracy":  accuracy_score(y_test, test_preds),
    "precision": precision_score(y_test, test_preds),
    "recall":    recall_score(y_test, test_preds),
    "f1":        f1_score(y_test, test_preds),
    "roc_auc":   roc_auc_score(y_test, test_probs),
}

# ← NEW: print the gap so you can spot overfitting immediately
print(f"\nCV ROC-AUC:   {best_cv_score:.4f}")
print(f"Test ROC-AUC: {test_metrics['roc_auc']:.4f}")
print(f"Gap:          {best_cv_score - test_metrics['roc_auc']:.4f}")
print("Test Metrics:", test_metrics)


# ===============================
# 5. SAVE MODEL + RESULTS
# ===============================
joblib.dump(best_model, MODEL_PATH)
print("Tuned model saved:", MODEL_PATH)

output = {
    "model":        "LogisticRegression",
    "best_params":  best_params,
    "cv_roc_auc":   best_cv_score,
    "test_metrics": test_metrics,
}
with open(RESULTS_PATH, "w") as f:
    json.dump(output, f, indent=4)
print("Tuning results saved:", RESULTS_PATH)
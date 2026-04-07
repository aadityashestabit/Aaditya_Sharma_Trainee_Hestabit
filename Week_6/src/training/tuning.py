import pandas as pd
import json
import optuna
import joblib
import os
import xgboost as xgb

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif

from src.pipelines.transformers import FeatureEngineer

optuna.logging.set_verbosity(optuna.logging.WARNING)  # cleaner output

# Path
DATA_PATH    = "src/data/processed/diabetes_clean.csv"
RESULTS_PATH = "src/tuning/tuning_results.json"
MODEL_PATH   = "src/models/tuned_model.pkl"

# Data Load
df = pd.read_csv(DATA_PATH)
X  = df.drop(columns=["Outcome"])
y  = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()


# Buuld pipeline around any model
def make_pipeline(model, k):
    return Pipeline([
        ("feature_engineering", FeatureEngineer()),
        ("scaler",              StandardScaler()),
        ("feature_selection",   SelectKBest(mutual_info_classif, k=k)),
        ("model",               model),
    ])


# Optuna objective functions 

# Logistic Regression
def objective_lr(trial):
    solver  = trial.suggest_categorical("solver", ["lbfgs", "liblinear", "saga"])
    penalty = "l2" if solver == "lbfgs" else trial.suggest_categorical("penalty", ["l1", "l2"])
    k       = trial.suggest_int("k", 6, 18)

    model = LogisticRegression(
        C            = trial.suggest_float("C", 0.01, 10.0, log=True),
        penalty      = penalty,
        solver       = solver,
        class_weight = trial.suggest_categorical("class_weight", ["balanced", None]),
        max_iter     = 5000,
        random_state = 42,
    )
    return cross_val_score(make_pipeline(model, k), X_train, y_train, cv=5, scoring="f1").mean()


# Random Forest 
def objective_rf(trial):
    k = trial.suggest_int("k", 6, 18)

    model = RandomForestClassifier(
        n_estimators     = trial.suggest_int("n_estimators", 100, 500, step=50),
        max_depth        = trial.suggest_int("max_depth", 3, 10),
        min_samples_leaf = trial.suggest_int("min_samples_leaf", 2, 20),
        min_samples_split= trial.suggest_int("min_samples_split", 5, 30),
        max_features     = trial.suggest_categorical("max_features", ["sqrt", "log2", 0.5]),
        max_samples      = trial.suggest_float("max_samples", 0.6, 1.0),
        class_weight     = "balanced",
        random_state     = 42,
    )
    return cross_val_score(make_pipeline(model, k), X_train, y_train, cv=5, scoring="f1").mean()


# XGB
def objective_xgb(trial):
    k = trial.suggest_int("k", 6, 18)

    model = xgb.XGBClassifier(
        n_estimators      = trial.suggest_int("n_estimators", 100, 500, step=50),
        max_depth         = trial.suggest_int("max_depth", 2, 8),
        learning_rate     = trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        subsample         = trial.suggest_float("subsample", 0.5, 1.0),
        colsample_bytree  = trial.suggest_float("colsample_bytree", 0.5, 1.0),
        reg_alpha         = trial.suggest_float("reg_alpha", 1e-4, 10.0, log=True),
        reg_lambda        = trial.suggest_float("reg_lambda", 1e-4, 10.0, log=True),
        scale_pos_weight  = scale_pos_weight,
        eval_metric       = "logloss",
        random_state      = 42,
        verbosity         = 0,
    )
    return cross_val_score(make_pipeline(model, k), X_train, y_train, cv=5, scoring="f1").mean()

#NN

def objective_nn(trial):
    k          = trial.suggest_int("k", 6, 18)
    n_layers   = trial.suggest_int("n_layers", 1, 3)
    layer_size = trial.suggest_categorical("layer_size", [32, 64, 128])
    hidden     = tuple([layer_size] * n_layers)

    model = MLPClassifier(
        hidden_layer_sizes = hidden,
        activation         = trial.suggest_categorical("activation", ["relu", "tanh"]),
        alpha              = trial.suggest_float("alpha", 1e-4, 0.1, log=True),
        learning_rate_init = trial.suggest_float("learning_rate_init", 1e-4, 0.01, log=True),
        early_stopping     = True,
        max_iter           = 500,
        random_state       = 42,
    )
    return cross_val_score(make_pipeline(model, k), X_train, y_train, cv=5, scoring="f1").mean()


#  RUN ALL STUDIES 
objectives = {
    "Logistic Regression": objective_lr,
    "Random Forest":       objective_rf,
    "XGBoost":             objective_xgb,
    "Neural Network":      objective_nn,
}

N_TRIALS = 50   # trials per model 

all_results = {}
best_overall_score = 0
best_overall_name  = ""
best_overall_params= {}

for name, objective_fn in objectives.items():
    print(f"\nTuning {name} ({N_TRIALS} trials)...")

    study = optuna.create_study(direction="maximize")
    study.optimize(objective_fn, n_trials=N_TRIALS, show_progress_bar=True)

    score  = study.best_value
    params = study.best_params

    print(f"  Best CV F1: {score:.4f}  |  Params: {params}")

    all_results[name] = {
        "cv_f1":       score,
        "best_params": params,
    }

    if score > best_overall_score:
        best_overall_score  = score
        best_overall_name   = name
        best_overall_params = params


print(f"\nBest model overall: {best_overall_name}  (CV F1 = {best_overall_score:.4f})")


#BUILD & TRAIN THE WINNING MODEL
best_k = best_overall_params.pop("k", 12)

model_constructors = {
    "Logistic Regression": lambda p: LogisticRegression(**p, max_iter=5000, random_state=42),
    "Random Forest":       lambda p: RandomForestClassifier(**p, class_weight="balanced", random_state=42),
    "XGBoost":             lambda p: xgb.XGBClassifier(**p, scale_pos_weight=scale_pos_weight,
                                                        eval_metric="logloss", random_state=42, verbosity=0),
    "Neural Network":      lambda p: MLPClassifier(**p, early_stopping=True, max_iter=500, random_state=42),
}

# Remove keys that were fixed in constructor not in trial params
final_model = model_constructors[best_overall_name](best_overall_params)
final_pipeline = make_pipeline(final_model, best_k)
final_pipeline.fit(X_train, y_train)
print("Final tuned pipeline trained")


# EVALUATE ON TEST SET 
test_preds = final_pipeline.predict(X_test)
test_probs = final_pipeline.predict_proba(X_test)[:, 1]

test_metrics = {
    "accuracy":  accuracy_score(y_test, test_preds),
    "precision": precision_score(y_test, test_preds),
    "recall":    recall_score(y_test, test_preds),
    "f1":        f1_score(y_test, test_preds),
    "roc_auc":   roc_auc_score(y_test, test_probs),
}

print(f"\nCV F1  (best model): {best_overall_score:.4f}")
print(f"Test F1:             {test_metrics['f1']:.4f}")
print(f"Gap:                 {best_overall_score - test_metrics['f1']:.4f}")
print(f"Test ROC-AUC:        {test_metrics['roc_auc']:.4f}")
print("Full test metrics:", test_metrics)


#SAVE 
os.makedirs("src/models",  exist_ok=True)
os.makedirs("src/tuning",  exist_ok=True)

joblib.dump(final_pipeline, MODEL_PATH)
print(f"\nTuned model saved: {MODEL_PATH}")

output = {
    "best_model":   best_overall_name,
    "best_k":       best_k,
    "best_params":  best_overall_params,
    "cv_f1":        best_overall_score,
    "test_metrics": test_metrics,
    "all_results":  all_results,
}

with open(RESULTS_PATH, "w") as f:
    json.dump(output, f, indent=4)

print(f"Tuning results saved: {RESULTS_PATH}")
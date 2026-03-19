import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns

from xgboost import XGBClassifier

# Paths
X_TRAIN_PATH = "src/data/features/X_train.csv"
Y_TRAIN_PATH = "src/data/features/y_train.csv"

X = pd.read_csv(X_TRAIN_PATH)
y = pd.read_csv(Y_TRAIN_PATH).squeeze()


# Train model
model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    eval_metric="logloss"
)

model.fit(X, y)


# SHAP explainability
explainer = shap.Explainer(model)

shap_values = explainer(X)


# SHAP summary plot
shap.summary_plot(shap_values, X, max_display=30 , show=False)

plt.savefig("src/evaluation/shap_summary.png")

print("SHAP summary plot saved")






importances = model.feature_importances_

feat_importance = pd.Series(importances, index=X.columns)

feat_importance = feat_importance.sort_values(ascending=False)

plt.figure(figsize=(10,5))

feat_importance.plot(kind="bar")

plt.title("Feature Importance")

plt.tight_layout()

plt.savefig("src/evaluation/feature_importance.png")

print("Feature importance plot saved")





preds = model.predict(X)

errors = (preds != y)

error_df = X.copy()

error_df["error"] = errors

corr = error_df.corr()

plt.figure(figsize=(8,6))

sns.heatmap(corr, cmap="coolwarm")

plt.title("Error Analysis Heatmap")

plt.savefig("src/evaluation/error_heatmap.png")

print("Error heatmap saved")
import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Paths
DATA_PATH = "src/data/processed/diabetes_clean.csv"
MODEL_PATH = "src/models/best_model.pkl"
OUTPUT_DIR = "src/evaluation"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===============================
# 1. LOAD DATA (RAW)
# ===============================
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["Outcome"])
y = df["Outcome"]


# ===============================
# 2. LOAD PIPELINE MODEL
# ===============================
pipeline = joblib.load(MODEL_PATH)

# Separate parts
feature_engineer = pipeline.named_steps["feature_engineering"]
scaler = pipeline.named_steps["scaler"]
model = pipeline.named_steps["model"]


# ===============================
# 3. TRANSFORM DATA (IMPORTANT)
# ===============================
X_transformed = feature_engineer.transform(X)
X_transformed = scaler.transform(X_transformed)

# Convert back to DataFrame for SHAP
X_transformed = pd.DataFrame(X_transformed,columns=feature_engineer.transform(X).columns) # to show features with names as they were scaled earlier and shown as numbers


# ===============================
# 4. SHAP EXPLAINABILITY
# ===============================
explainer = shap.LinearExplainer(model,X_transformed)
shap_values = explainer(X_transformed)

# Summary plot
shap.summary_plot(shap_values, X_transformed, max_display=20, show=False)
plt.savefig(f"{OUTPUT_DIR}/shap_summary.png")
plt.close()

print("SHAP summary plot saved")


# ===============================
# 5. FEATURE IMPORTANCE
# ===============================
importances = model.coef_[0]

feat_importance = pd.Series(importances, index=X_transformed.columns)
feat_importance = feat_importance.sort_values(ascending=False)

plt.figure(figsize=(10, 5))
feat_importance.plot(kind="bar")
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/feature_importance.png")
plt.close()

print("Feature importance plot saved")


# ===============================
# 6. ERROR ANALYSIS
# ===============================
preds = model.predict(X_transformed)
errors = (preds != y)

error_df = X_transformed.copy()
error_df["error"] = errors

corr = error_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, cmap="coolwarm")
plt.title("Error Analysis Heatmap")
plt.savefig(f"{OUTPUT_DIR}/error_heatmap.png")
plt.close()

print("Error heatmap saved")
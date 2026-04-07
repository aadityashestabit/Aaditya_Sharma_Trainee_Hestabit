import pandas as pd
import shap
import matplotlib.pyplot as plt
import joblib
import os
from sklearn.model_selection import train_test_split

# Paths
DATA_PATH  = "src/data/processed/diabetes_clean.csv"
MODEL_PATH = "src/models/tuned_model.pkl"
OUTPUT_DIR = "src/evaluation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data Load
df = pd.read_csv(DATA_PATH)
X  = df.drop(columns=["Outcome"])
y  = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline loading 
pipeline = joblib.load(MODEL_PATH)

feature_engineer = pipeline.named_steps["feature_engineering"]
scaler           = pipeline.named_steps["scaler"]
selector         = pipeline.named_steps["feature_selection"]
model            = pipeline.named_steps["model"]

# Transform
X_eng      = feature_engineer.transform(X_test)
X_scaled   = scaler.transform(X_eng)
X_selected = selector.transform(X_scaled)

all_feature_names      = feature_engineer.get_feature_names_out()
selected_indices       = selector.get_support(indices=True)
selected_feature_names = [all_feature_names[i] for i in selected_indices]

X_shap = pd.DataFrame(X_selected, columns=selected_feature_names)

# Shap summary 
explainer   = shap.TreeExplainer(model)
shap_values = explainer(X_shap)

shap.summary_plot(shap_values, X_shap, max_display=15, show=False)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/shap_summary.png", bbox_inches="tight")
plt.close()

print("SHAP summary plot saved")
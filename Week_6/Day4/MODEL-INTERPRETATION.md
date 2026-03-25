# Model Interpretation Report

## Overview
This document provides an interpretation of the final selected model after hyperparameter tuning. The goal is to understand how tuning impacted performance, what the model is learning, and why this model was chosen for deployment.

---

## Best Model Configuration

- Model: Logistic Regression
- Solver: liblinear
- Penalty: l1
- Regularization Strength (C): 0.2765
- Class Weight: balanced

---

## Performance Comparison

### Before Tuning vs After Tuning

| Metric        | Before Tuning | After Tuning |
|--------------|--------------|--------------|
| Accuracy     | 0.7792       | 0.7727       |
| Precision    | 0.7442       | 0.6462       |
| Recall       | 0.5818       | 0.7778       |
| F1 Score     | 0.6531       | 0.7059       |
| ROC AUC      | 0.8123       | 0.8350       |
| CV F1 Score  | 0.6923       | 0.6995       |

---

## Key Observations

- **Recall significantly improved** after tuning (from 0.58 to 0.78), indicating the model is now better at identifying positive cases.
- **F1 score increased**, showing a better balance between precision and recall.
- **ROC AUC improved**, meaning the model has better overall class separation capability.
- **Precision decreased**, which is expected due to the increase in recall. The model is now slightly more permissive in predicting positive cases.
- **CV F1 score improved**, indicating better generalization across different data splits.

---

## Effect of Hyperparameters

### L1 Regularization (Lasso)
- Encourages sparsity in model coefficients.
- Helps in feature selection by reducing less important feature weights to zero.
- Reduces overfitting and improves interpretability.

### Lower C Value (Stronger Regularization)
- A smaller C value increases regularization strength.
- Prevents the model from fitting noise in the data.
- Leads to a simpler and more generalizable model.

### Class Weight = Balanced
- Adjusts weights inversely proportional to class frequencies.
- Helps in handling class imbalance.
- Improves recall for the minority class.

### Solver = liblinear
- Works well for smaller datasets.
- Supports L1 regularization efficiently.

---

## Bias-Variance Tradeoff

- Before tuning, the model had **higher bias toward precision**, missing many positive cases.
- After tuning, the model achieves a **better balance**, reducing bias and slightly increasing variance.
- Cross-validation performance improvement indicates that variance is still under control.

---

## Final Model Behavior

- The model is now more **recall-oriented**, making it suitable for problems where missing positive cases is costly.
- It generalizes better due to improved cross-validation performance.
- The use of L1 regularization ensures that the model remains **interpretable and not overly complex**.

---
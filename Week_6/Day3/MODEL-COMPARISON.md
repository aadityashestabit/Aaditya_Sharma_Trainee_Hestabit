# Model Evaluation Report

## Overview
This document summarizes the performance of multiple machine learning models trained and evaluated on the dataset. The models compared include Logistic Regression, Random Forest, XGBoost, and a Neural Network.

The evaluation is based on standard classification metrics, with special emphasis on cross-validation F1 score (cv_f1) for model selection.

---

## Evaluation Metrics Table

| Model                | Accuracy | Precision | Recall  | F1 Score | ROC AUC | CV F1 Score |
|---------------------|----------|----------|---------|----------|---------|-------------|
| Logistic Regression | 0.7792   | 0.7442   | 0.5818  | 0.6531   | 0.8123  | 0.6923      |
| Random Forest       | 0.7468   | 0.7857   | 0.4000  | 0.5301   | 0.8253  | 0.6489      |
| XGBoost             | 0.7857   | 0.6964   | 0.7091  | 0.7027   | 0.8206  | 0.6427      |
| Neural Network      | 0.7468   | 0.6905   | 0.5273  | 0.5979   | 0.7857  | 0.6515      |

---

## Model Selection Strategy

The primary criterion for selecting the best model is the **cross-validation F1 score (cv_f1)**.

### Why CV F1 Score?

- F1 score balances **precision and recall**, making it suitable for imbalanced datasets.
- Cross-validation ensures that the model performance is **consistent across different data splits**, reducing the risk of overfitting.
- It provides a more **robust estimate of real-world performance** compared to a single train-test split.

---

## Observations

- **Logistic Regression** achieved the highest CV F1 score (0.6923), indicating strong generalization performance.
- **XGBoost** has the highest test F1 score (0.7027), but its lower CV F1 suggests possible overfitting or instability across folds.
- **Random Forest** shows high precision but very low recall, meaning it misses many positive cases.
- **Neural Network** performs moderately across all metrics but does not outperform other models.

---

## Final Model Selection

Based on the evaluation, **Logistic Regression** is selected as the final model due to its highest cross-validation F1 score and stable performance across different data splits.

---

## Conclusion

While more complex models like XGBoost and Neural Networks can capture non-linear patterns, simpler models like Logistic Regression can sometimes generalize better depending on the dataset. 

Selecting a model based on cross-validation metrics ensures better reliability and robustness in production environments.
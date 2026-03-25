```
.
├── DATA-REPORT.md
├── DEPLOYMENT-NOTES.md
├── Dockerfile
├── download_dataset.py
├── FEATURE_ENGINEERING_DOC.md
├── MODEL-COMPARISON.md
├── MODEL-INTERPRETATION.md
├── requirements.txt
└── src
    ├── config
    ├── data
    │   ├── features
    │   │   ├── X_test.csv
    │   │   ├── X_train.csv
    │   │   ├── y_test.csv
    │   │   └── y_train.csv
    │   ├── processed
    │   │   └── diabetes_clean.csv
    │   └── raw
    │       └── diabetes.csv
    ├── deployment
    │   ├── api.py
    ├── evaluation
    │   ├── confusion_matrix.png
    │   ├── metrics.json
    │   └── shap_analysis.py
    ├── features
    │   ├── feature_list.json
    │   ├── feature_selector.py
    │   └── selected_features.json
    ├── logs
    │   ├── correlation_matrix.png
    │   ├── feature_distributions.png
    │   ├── missing_values_heatmap.png
    │   └── target_distribution.png
    ├── models
    │   ├── best_model.pkl
    │   └── tuned_model.pkl
    ├── monitoring
    │   └── drift_checker.py
    ├── notebooks
    │   ├── EDA.ipynb
    │   ├── EDA_practice.ipynb
    │   └── EDA_raw_data.ipynb
    ├── pipelines
    │   ├── data_pipeline.py
    │   └── transformers.py
    ├── prediction_logs.csv
    ├── training
    │   ├── train.py
    │   └── tuning.py
    ├── tuning
    │   └── tuning_results.json
    └── utils

```
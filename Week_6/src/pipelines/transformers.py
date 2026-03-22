import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # Feature Engineering
        X["AgeGroup"] = pd.cut(
            X["Age"],
            bins=[0, 30, 45, 60, 100],
            labels=["Young", "Adult", "MiddleAge", "Senior"]
        )

        X["BMICategory"] = pd.cut(
            X["BMI"],
            bins=[0, 18.5, 25, 30, 100],
            labels=["Underweight", "Normal", "Overweight", "Obese"]
        )

        X["HighGlucose"] = (X["Glucose"] > 140).astype(int)
        X["HighBP"] = (X["BloodPressure"] > 90).astype(int)
        X["MultiplePregnancies"] = (X["Pregnancies"] >= 3).astype(int)

        X["BMI_Age"] = X["BMI"] * X["Age"]
        X["Glucose_BMI"] = X["Glucose"] * X["BMI"]
        X["Age_Glucose"] = X["Age"] * X["Glucose"]

        # Log transforms
        X["DPF_log"] = np.log1p(X["DiabetesPedigreeFunction"])
        X["Age_log"] = np.log1p(X["Age"])

        # Drop original
        X.drop(columns=["DiabetesPedigreeFunction", "Age"], inplace=True)

        # Encoding
        X = pd.get_dummies(X, columns=["AgeGroup", "BMICategory"], drop_first=True)

        return X
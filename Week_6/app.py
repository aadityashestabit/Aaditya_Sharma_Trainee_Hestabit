import streamlit as st
import pandas as pd
import joblib
import requests


API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="Diabetes Predictor", layout="wide")


# HEADER

st.markdown(
    "<h1 style='text-align: center;'>🩺 Diabetes Prediction Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

st.sidebar.title("ℹ️ About")
st.sidebar.write("This app predicts diabetes risk using a trained ML model.")


# INPUT SECTION 


col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose", 0, 500, 120)
    bp = st.number_input("Blood Pressure", 0, 220, 70)

with col2:
    bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
    dpf = st.number_input("Diabetes Pedigree Function", value=0.5)
    age = st.number_input("Age", 1, 120, 30)

st.markdown("---")


# PREDICTION


# ===============================
# PREDICTION
# ===============================

if st.button("🔍 Predict", use_container_width=True):

    input_data = pd.DataFrame({
        "Pregnancies": [pregnancies],
        "Glucose": [glucose],
        "BloodPressure": [bp],
        "BMI": [bmi],
        "DiabetesPedigreeFunction": [dpf],
        "Age": [age]
    })

    try:
        response = requests.post(
            API_URL,
            json=input_data.to_dict(orient="records")[0]
        )

        #  Check if API worked
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
        else:
            result = response.json()

            # Check key exists
            if "prediction" not in result:
                st.error("Invalid API response")
                st.write(result)
            else:
                st.write(result)
                prediction = result["prediction"]

                st.markdown("## 📊 Prediction Result")

                if prediction == 1:
                    st.error("🚨 High Risk of Diabetes")
                else:
                    st.success("✅ Low Risk of Diabetes")

                st.markdown("---")
                st.write("###  Model Insight")
                st.write(
                    "The model predicts diabetes risk based on input health parameters."
                )

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI server is not running")

    except Exception as e:
        st.error("Unexpected error occurred")
        st.write(e)
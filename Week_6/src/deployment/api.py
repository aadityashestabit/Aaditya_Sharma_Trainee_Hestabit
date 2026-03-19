from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import uuid
import datetime

MODEL_PATH = "src/models/best_model.pkl"
LOG_PATH = "src/logs/prediction_logs.csv"

app = FastAPI()

# Load model
model = joblib.load(MODEL_PATH)


# Input schema
class PatientData(BaseModel):


  Pregnancies: float
  Glucose: float
  BloodPressure: float
  SkinThickness: float
  Insulin: float
  BMI: float
  DiabetesPedigreeFunction: float
  Age: float
  HighGlucose: float
  HighBP: float
  BMI_Age: float
  Insulin_Glucose_Ratio: float
  MultiplePregnancies: float
  Skin_BMI_Ratio: float
  Glucose_BMI: float
  Age_Glucose: float
  AgeGroup_Adult: float
  AgeGroup_MiddleAge: float
  AgeGroup_Senior: float
  BMICategory_Normal: float
  BMICategory_Overweight: float
  BMICategory_Obese: float



@app.get("/")
def home():
    return {"message": "Diabetes Prediction API"}


@app.post("/predict")
def predict(data: PatientData):

    request_id = str(uuid.uuid4())

    input_df = pd.DataFrame([data.dict()])

    prediction = model.predict(input_df)[0]

    log = {
        "request_id": request_id,
        "timestamp": datetime.datetime.now(),
        "prediction": int(prediction)
    }

    log_df = pd.DataFrame([log])

    try:
        old_logs = pd.read_csv(LOG_PATH)
        log_df = pd.concat([old_logs, log_df])
    except:
        pass

    log_df.to_csv(LOG_PATH, index=False)

    return {
        "request_id": request_id,
        "prediction": int(prediction)
    }
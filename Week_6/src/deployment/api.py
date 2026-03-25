from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import uuid
import datetime
import os
from pathlib import Path

# Paths
MODEL_PATH = "src/models/best_model.pkl"

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = (BASE_DIR / "../prediction_logs.csv").resolve()

os.makedirs(LOG_PATH.parent, exist_ok=True)

# Initialize app
app = FastAPI(title="Diabetes Prediction API")

# Load pipeline (IMPORTANT: this is pipeline now, not just model)
model = joblib.load(MODEL_PATH)


# RAW inout that will be provided to the api to test 
class PatientData(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float


# Health check - get route 
@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running"}  


# Prediction endpoint - post route 
@app.post("/predict")
def predict(data: PatientData): # --> passing patient data as body to api 

    request_id = str(uuid.uuid4()) 

    # Convert input to DataFrame
    input_df = pd.DataFrame([data.model_dump()])

    # Pipeline handles everything now
    prediction = model.predict(input_df)[0]

    # Logging
    log = {
        "request_id": request_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "prediction": int(prediction),
        **data.model_dump()
    }

    log_df = pd.DataFrame([log])

    log_df.to_csv(
        LOG_PATH,
        mode='a',
        header=not LOG_PATH.exists(),
        index=False
    )

    return {
        "request_id": request_id,
        "prediction": int(prediction)
    }
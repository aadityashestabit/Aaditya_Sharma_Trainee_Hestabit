# Deployment Notes

## Overview
The system is built using FastAPI and packaged inside a Docker container for consistent and reproducible deployment.

The deployed service exposes endpoints for health checks and predictions, while also logging all prediction requests for monitoring and analysis.

---

## Project Structure (Relevant Components)

- src/deployment/api.py → FastAPI application
- src/models/tuned_model.pkl → Trained ML pipeline
- prediction_logs.csv → Stores inference logs
- Dockerfile → Container configuration

---

## API Design

### Base URL
http://localhost:8000

### Endpoints

#### 1. Health Check
- Method: GET
- Endpoint: /

Response:
{
  "message": "Diabetes Prediction API is running"
}

---

#### 2. Prediction Endpoint
- Method: POST
- Endpoint: /predict

Request Body:
```
{
"Pregnancies": float,
"Glucose": float,
"BloodPressure": float,
"BMI": float,
"DiabetesPedigreeFunction": float,
"Age": float
}
```

Response:

```
{
"request_id": "unique-id",
"prediction": 0 or 1
}
```


---

## Inference Flow

1. User sends input data to /predict endpoint
2. Data is validated using Pydantic schema (PatientData)
3. Input is converted into a Pandas DataFrame
4. Pre-trained pipeline (including preprocessing + model) is loaded using joblib
5. Prediction is generated
6. Request details and prediction are logged into a CSV file
7. Response is returned with prediction and request ID

---

## Logging Mechanism

- Each request is assigned a unique request_id using UUID
- Timestamp is recorded for tracking
- Input features and prediction are stored
- Logs are appended to:
  prediction_logs.csv

Purpose of logging:
- Monitor model predictions
- Detect data drift
- Debug incorrect predictions

---

## Model Serving Strategy

- The saved object is a full **pipeline**, not just a model
- Pipeline handles:
  - Preprocessing
  - Feature engineering
  - Prediction

Benefits:
- No need to manually preprocess input data
- Reduces chances of training-serving skew
- Ensures consistency between training and inference

---

## Docker Configuration

### Base Image
python:3.10

### Working Directory
/app

### Installed Dependencies
- fastapi
- uvicorn
- pandas
- scikit-learn
- joblib
- pydantic

### Environment Variable
PYTHONPATH=/app

### Run Command

```
uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000
```


---

## How to Build and Run

### Build Docker Image
```
docker build -t diabetes-api .
```

### Run Container

```
docker run -p 8000:8000 diabetes-api
```


API will be available at:
http://localhost:8000

---

## Key Design Decisions

- Used FastAPI for high performance and automatic validation
- Used Pydantic for strict input schema validation
- Used pipeline instead of raw model to avoid preprocessing mismatch
- Implemented request logging for monitoring and future analysis
- Containerized using Docker for portability and scalability

---




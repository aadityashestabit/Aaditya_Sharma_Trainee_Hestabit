FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pandas scikit-learn joblib pydantic

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]
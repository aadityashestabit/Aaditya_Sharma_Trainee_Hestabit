# Build:  docker build -t medical-llm-api .
# Run:    docker run -p 8000:8000 -v /path/to/model.gguf:/app/model.gguf medical-llm-api

FROM python:3.11-slim

WORKDIR /app

# install system dependencies needed for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app files
COPY app.py .
COPY model_loader.py .
COPY config.py .

# model.gguf is mounted at runtime via docker -v flag
# so we don't copy it into the image

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
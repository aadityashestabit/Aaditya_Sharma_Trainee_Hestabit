# config.py
# All settings for the API server in one place.
# Change MODEL_PATH to wherever your model.gguf is stored.

import os

# Model settings
MODEL_PATH    = os.getenv("MODEL_PATH", "model.gguf")  # path to your model.gguf
N_CTX         = 2048       # context window size
N_THREADS     = 4          # CPU threads to use
N_GPU_LAYERS  = 0          # 0 = CPU only, -1 = all layers on GPU

#Generation defaults
DEFAULT_MAX_TOKENS  = 200
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P       = 0.95
DEFAULT_TOP_K       = 40
DEFAULT_REPEAT_PENALTY = 1.3

# Server settings 
HOST = "0.0.0.0"
PORT = 8000

#System prompt 
SYSTEM_PROMPT = "You are a helpful medical assistant. Answer clearly and accurately. if you dont have context then just say question out of knowledge"
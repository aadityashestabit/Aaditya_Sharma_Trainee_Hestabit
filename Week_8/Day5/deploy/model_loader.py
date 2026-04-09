# model_loader.py
# Loads the GGUF model once and keeps it in memory.
# All API routes share the same loaded model instance.

from llama_cpp import Llama
import config

# this variable holds the model after it is loaded
_model = None

def load_model():
    """
    Load the GGUF model into memory.
    Called once when the server starts.
    """
    global _model

    try:
        print(f"⏳ Loading model from {config.MODEL_PATH}...")
        _model = Llama(
            model_path    = config.MODEL_PATH,
            n_ctx         = config.N_CTX,
            n_threads     = config.N_THREADS,
            n_gpu_layers  = config.N_GPU_LAYERS,
            verbose       = False
        )
        print("Model loaded and ready")
        return True

    except Exception as e:
        print(f" Failed to load model: {e}")
        return False


def get_model():
    """
    Return the loaded model.
    Raises an error if model was not loaded yet.
    """
    if _model is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")
    return _model
# app.py
# FastAPI inference server for our fine-tuned medical LLM
#
# Endpoints:
#   POST /generate  - single prompt, single response
#   POST /chat      - multi-turn conversation with history
#
# Run with:
#   uvicorn app:app --host 0.0.0.0 --port 8000

import uuid
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import config
import model_loader

# Setup loggin
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Medical LLM API",
    description="Fine-tuned TinyLlama medical assistant — Week 8 Day 5",
    version="1.0.0"
)

# Request/Response models

class GenerateRequest(BaseModel):
    prompt:      str
    max_tokens:  Optional[int]   = config.DEFAULT_MAX_TOKENS
    temperature: Optional[float] = config.DEFAULT_TEMPERATURE
    top_p:       Optional[float] = config.DEFAULT_TOP_P
    top_k:       Optional[int]   = config.DEFAULT_TOP_K
    stream:      Optional[bool]  = False
    system:      Optional[str]   = config.SYSTEM_PROMPT


class ChatMessage(BaseModel):
    role:    str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages:    List[ChatMessage]
    max_tokens:  Optional[int]   = config.DEFAULT_MAX_TOKENS
    temperature: Optional[float] = config.DEFAULT_TEMPERATURE
    top_p:       Optional[float] = config.DEFAULT_TOP_P
    top_k:       Optional[int]   = config.DEFAULT_TOP_K
    stream:      Optional[bool]  = False
    system:      Optional[str]   = config.SYSTEM_PROMPT


# Helper: build prompt from messages

def build_chat_prompt(messages: List[ChatMessage], system: str) -> str:
    """
    Convert a list of messages into TinyLlama chat format:
    <|system|>
    You are a helpful medical assistant.
    <|user|>
    Patient question here
    <|assistant|>
    """
    prompt = f"<|system|>\n{system}\n"
    for msg in messages:
        if msg.role == "user":
            prompt += f"<|user|>\n{msg.content}\n"
        elif msg.role == "assistant":
            prompt += f"<|assistant|>\n{msg.content}\n"
    prompt += "<|assistant|>\n"
    return prompt


def build_generate_prompt(user_prompt: str, system: str) -> str:
    """Build a simple single-turn prompt."""
    return (
        f"<|system|>\n{system}\n"
        f"<|user|>\n{user_prompt}\n"
        f"<|assistant|>\n"
    )


# ── Startup: load model ────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    success = model_loader.load_model()
    if not success:
        raise RuntimeError("Could not load model. Check MODEL_PATH in config.py")


# Routes

@app.get("/")
def root():
    return {
        "status":  "running",
        "model":   config.MODEL_PATH,
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/generate")
def generate(req: GenerateRequest):
    """
    Single turn generation.
    Send a prompt, get a response back.

    Example:
        POST /generate
        {
            "prompt": "What are symptoms of diabetes?",
            "temperature": 0.7,
            "max_tokens": 200
        }
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] /generate | prompt: {req.prompt[:50]}...")

    try:
        model  = model_loader.get_model()
        prompt = build_generate_prompt(req.prompt, req.system)

        # streaming response
        if req.stream:
            def stream_tokens():
                try:
                    for chunk in model(
                        prompt,
                        max_tokens  = req.max_tokens,
                        temperature = req.temperature,
                        top_p       = req.top_p,
                        top_k       = req.top_k,
                        repeat_penalty = 1.3,
                        stop        = ["<|user|>", "<|system|>"],
                        stream      = True
                    ):
                        token = chunk["choices"][0]["text"]
                        yield token
                except Exception as e:
                    yield f"\n[Error: {e}]"

            return StreamingResponse(stream_tokens(), media_type="text/plain")

        # normal response
        output   = model(
            prompt,
            max_tokens  = req.max_tokens,
            temperature = req.temperature,
            top_p       = req.top_p,
            top_k       = req.top_k,
            repeat_penalty = 1.3,
            stop        = ["<|user|>", "<|system|>"]
        )
        response = output["choices"][0]["text"].strip()
        tokens   = output["usage"]["completion_tokens"]

        logger.info(f"[{request_id}] generated {tokens} tokens")

        return {
            "request_id": request_id,
            "response":   response,
            "tokens":     tokens,
            "model":      config.MODEL_PATH
        }

    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat(req: ChatRequest):
    """
    Multi-turn chat with conversation history.
    Send full message history, get next assistant response.

    Example:
        POST /chat
        {
            "messages": [
                {"role": "user", "content": "What is diabetes?"},
                {"role": "assistant", "content": "Diabetes is..."},
                {"role": "user", "content": "How is it treated?"}
            ]
        }
    """
    request_id = str(uuid.uuid4())[:8]
    last_msg   = req.messages[-1].content if req.messages else ""
    logger.info(f"[{request_id}] /chat | messages: {len(req.messages)} | last: {last_msg[:50]}")

    try:
        model  = model_loader.get_model()
        prompt = build_chat_prompt(req.messages, req.system)

        # streaming response
        if req.stream:
            def stream_tokens():
                try:
                    for chunk in model(
                        prompt,
                        max_tokens  = req.max_tokens,
                        temperature = req.temperature,
                        top_p       = req.top_p,
                        top_k       = req.top_k,
                        repeat_penalty = 1.3,
                        stop        = ["<|user|>", "<|system|>"],
                        stream      = True
                    ):
                        token = chunk["choices"][0]["text"]
                        yield token
                except Exception as e:
                    yield f"\n[Error: {e}]"

            return StreamingResponse(stream_tokens(), media_type="text/plain")

        # normal response
        output   = model(
            prompt,
            max_tokens  = req.max_tokens,
            temperature = req.temperature,
            top_p       = req.top_p,
            top_k       = req.top_k,
            stop        = ["<|user|>", "<|system|>"]
        )
        response = output["choices"][0]["text"].strip()
        tokens   = output["usage"]["completion_tokens"]

        logger.info(f"[{request_id}] generated {tokens} tokens")

        return {
            "request_id": request_id,
            "response":   response,
            "tokens":     tokens,
            "model":      config.MODEL_PATH
        }

    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
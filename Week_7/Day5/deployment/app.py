import os
import json
from datetime import datetime
from groq import Groq
from src.pipelines.context_builder import build_context
from src.pipelines.sql_pipeline import ask_sql
from src.retriever.image_search import search_by_text, search_by_image
from src.memory.memory_store import get_memory, add_message
from src.evaluation.rag_eval import evaluate, refine_answer

try:
    os.makedirs("src/logs", exist_ok=True)
except:
    pass

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_FILE   = os.path.join(BASE_DIR, "src", "memory", "chat_memory.json")
CHAT_LOG_FILE = os.path.join(BASE_DIR, "src", "logs", "CHAT-LOGS.json")

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except:
    client = None

MODEL = "llama-3.3-70b-versatile"

# log chats in CHAT-LOGS.json
def log_chat(entry):
    try:
        logs = []
        if os.path.exists(CHAT_LOG_FILE):
            with open(CHAT_LOG_FILE) as f:
                logs = json.load(f)
        logs.append(entry)
        with open(CHAT_LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
    except:
        pass

# text rag entrypoint
def ask(question):
    # retrieve context  hybrid search - filter CSV - rerank - deduplicate - format.
    try:
        context_data = build_context(question)
        context      = context_data["context"]
        sources      = context_data["sources"]
        memory       = get_memory()
    except:
        return {"answer": "", "sources": [], "evaluation": {}}

    try:
        messages = [{"role": "system", "content": f"""You are an enterprise document assistant.
You answer questions strictly based on the provided context documents.
You are NOT a person and do NOT have a name.
If someone asks who you are, say you are an AI assistant.
If the answer is not in the context, say "I don't have enough information."

CONTEXT:
{context}"""}]
        messages += memory
        messages.append({"role": "user", "content": question})
    except:
        return {"answer": "", "sources": [], "evaluation": {}}

    try:
        answer = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=0.2
        ).choices[0].message.content.strip()
    except:
        answer = ""

    try:
        clean_chunks = []
        for chunk in context.split("\n\n"):
            chunk = chunk.strip()
            if not chunk:
                continue
            if chunk.startswith("[Source"):
                chunk = "\n".join(chunk.split("\n")[1:]).strip()
            if chunk:
                clean_chunks.append({"text": chunk})
    except:
        clean_chunks = []

    try:
        scores = evaluate(answer, clean_chunks)
        answer = refine_answer(answer, clean_chunks)
    except:
        scores = {"faithfulness": 0.5, "confidence": 0.5, "hallucination_risk": "MEDIUM"}

    try:
        add_message("user", question)
        add_message("assistant", answer)
    except:
        pass

    try:
        log_chat({
            "timestamp":          datetime.now().isoformat(),
            "type":               "ask",
            "question":           question,
            "answer":             answer,
            "sources":            sources,
            "faithfulness":       scores["faithfulness"],
            "confidence":         scores["confidence"],
            "hallucination_risk": scores["hallucination_risk"]
        })
    except:
        pass

    return {
        "answer":             answer,
        "sources":            sources,
        "evaluation":         scores
    }


# image rag 
def ask_image(query=None, image_path=None, mode="text"):
    
    # prevent empty search queries 
    if mode == "text" and (not query or not query.strip()):
        return {"answer": "Please enter a search query.", "context_used": []}

    try:
        if mode == "text":
            results = search_by_text(query, top_k=3)
        else:
            results = search_by_image(image_path, top_k=3)
    except:
        return {"answer": "", "context_used": []}

    if not results:
        return {"answer": "No relevant images found", "context_used": []}

    # Image→Image — just return results, no LLM needed
    if mode == "image" and not query:
        return {
            "answer":       f"Found {len(results)} similar images.",
            "context_used": [{
                "source":   r["image_path"],
                "caption":  r["caption"],
                "ocr_text": r.get("ocr_text", ""),
                "score":    r["score"]
            } for r in results]
        }

    # Text - Image or Image - Text — call Groq
    try:
        image_context = "\n".join([
            f"Image: {os.path.basename(r['image_path'])}\nCaption: {r['caption']}\nOCR: {r.get('ocr_text', '')}"
            for r in results
        ])
    except:
        image_context = ""

    try:
        prompt = query or "Extract and describe all text and content visible in this image"
    except:
        prompt = ""

    try:
        answer = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": f"""You are an enterprise document assistant.
Answer based on these images only.
If the answer is not in the images, say "I don't have enough information."

QUESTION: {prompt}
IMAGES:
{image_context}"""}],
            temperature=0.3 # temp
        ).choices[0].message.content.strip()
    except:
        answer = ""

    try:
        log_chat({
            "timestamp": datetime.now().isoformat(),
            "type":      f"ask-image-{mode}",
            "question":  prompt,
            "answer":    answer
        })
    except:
        pass

    return {
        "answer":       answer,
        "context_used": [{
            "source":   r["image_path"],
            "caption":  r["caption"],
            "ocr_text": r.get("ocr_text", ""),
            "score":    r["score"]
        } for r in results]
    }
    
def ask_sql_endpoint(question):
    try:
        result = ask_sql(question)
    except:
        result = {}

    try:
        log_chat({
            "timestamp": datetime.now().isoformat(),
            "type": "ask-sql",
            "question": question,
            "sql": result.get("sql", ""),
            "answer": result.get("answer", ""),
            "error": result.get("error")
        })
    except:
        pass

    return result

if __name__ == "__main__":
    try:
        print("=== /ask ===")
        r = ask("What is the minimum internet speed for working from home?")
        print(f"Answer: {r['answer'][:200]}")
        print(f"Evaluation: {r['evaluation']}")

        print("\n=== /ask-image text mode ===")
        r = ask_image(query="dog breeds", mode="text")
        print(f"Answer: {r['answer'][:200]}")

        print("\n=== /ask-sql ===")
        r = ask_sql_endpoint("How many customers are there in total?")
        print(f"Answer: {r.get('answer', '')}")
    except:
        pass
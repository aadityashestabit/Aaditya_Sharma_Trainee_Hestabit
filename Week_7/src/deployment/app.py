import os
import json
from datetime import datetime
from groq import Groq
from src.pipelines.context_builder import build_context
from src.pipelines.sql_pipeline import ask_sql
from src.retriever.image_search import search_by_text
from src.memory.memory_store import get_memory, add_message, clear_memory
from src.evaluation.rag_eval import score_faithfulness, detect_hallucination

os.makedirs("src/logs", exist_ok=True)
CHAT_LOG_FILE = "src/logs/CHAT-LOGS.json"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

def log_chat(entry):
    logs = []
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append(entry)
    with open(CHAT_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def ask(question):
    # Step 1 — get memory
    memory = get_memory()

    # Step 2 — build context from documents
    context_data = build_context(question)
    context      = context_data["context"]
    sources      = context_data["sources"]

    # Step 3 — build messages with memory + context
    system_prompt = f"""You are a helpful enterprise assistant. 
Answer the user's question based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information to answer this."

CONTEXT:
{context}"""

    messages = [{"role": "system", "content": system_prompt}]
    messages += memory  # add last 5 messages
    messages.append({"role": "user", "content": question})

    # Step 4 — generate answer
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )
    answer = response.choices[0].message.content.strip()

    # Step 5 — evaluate faithfulness
    faith_score = score_faithfulness(question, context, answer)
    hall_risk   = detect_hallucination(faith_score)

    # Step 6 — save to memory and log
    add_message("user", question)
    add_message("assistant", answer)

    log_chat({
        "timestamp":         datetime.now().isoformat(),
        "type":              "ask",
        "question":          question,
        "answer":            answer,
        "sources":           sources,
        "faithfulness":      faith_score,
        "hallucination_risk": hall_risk
    })

    return {
        "answer":            answer,
        "sources":           sources,
        "faithfulness":      faith_score,
        "hallucination_risk": hall_risk
    }

def ask_image(query):
    results = search_by_text(query, top_k=3)
    if not results:
        return {"answer": "No relevant images found.", "images": []}

    # build context from image captions and OCR
    image_context = ""
    for r in results:
        image_context += f"Image: {r['filename']}\n"
        image_context += f"Caption: {r['caption']}\n"
        image_context += f"OCR Text: {r['ocr_text']}\n\n"

    prompt = f"""Based on these images found in the knowledge base, answer the question.

QUESTION: {query}

IMAGES FOUND:
{image_context}

Answer based on what the images contain."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    answer = response.choices[0].message.content.strip()

    log_chat({
        "timestamp": datetime.now().isoformat(),
        "type":      "ask-image",
        "question":  query,
        "answer":    answer,
        "images":    [r["filename"] for r in results]
    })

    return {"answer": answer, "images": results}

def ask_sql_endpoint(question):
    result = ask_sql(question)
    log_chat({
        "timestamp": datetime.now().isoformat(),
        "type":      "ask-sql",
        "question":  question,
        "sql":       result.get("sql", ""),
        "answer":    result.get("answer", ""),
        "error":     result.get("error", None)
    })
    return result

if __name__ == "__main__":
    print("=== Testing /ask ===")
    result = ask("How much minimum speed for work from home")
    print(f"Answer: {result['answer'][:200]}")
    print(f"Faithfulness: {result['faithfulness']}")
    print(f"Hallucination risk: {result['hallucination_risk']}")

    print("\n=== Testing /ask-image ===")
    result = ask_image("How many total dog breed")
    print(f"Answer: {result['answer'][:200]}")

    print("\n=== Testing /ask-sql ===")
    result = ask_sql_endpoint("How many customers are there in total?")
    print(f"Answer: {result.get('answer', '')}")
# Deployment Notes — Day 5 (Capstone)

## What Day 5 Builds

Day 5 ties everything from Day 1 to Day 4 into a single working system with:
- Conversational memory (last 5 messages)
- Three endpoints — `/ask`, `/ask-image`, `/ask-sql`
- Faithfulness scoring to detect hallucination
- Full chat logging to `CHAT-LOGS.json`
- Streamlit UI to interact with everything

---

## System Architecture

```
                        ┌──────────────────────────────────┐
                        │         Streamlit UI             │
                        │  /ask  |  /ask-image  |  /ask-sql│
                        └────────────────┬─────────────────┘
                                         │
                        ┌────────────────▼─────────────────┐
                        │          app.py (router)         │
                        └──┬─────────────┬────────────┬────┘
                           │             │            │
              ┌────────────▼──┐   ┌──────▼────-┐  ┌───▼──────────┐
              │context_builder│   │image_search│  │ sql_pipeline │
              │(Day 2 hybrid) │   │ (Day 3)    │  │  (Day 4)     │
              └────────────┬──┘   └──────┬────-┘  └───┬──────────┘
                           │             │            │
                        ┌──▼─────────────▼────────────▼──┐
                        │         Groq LLM               │
                        │   llama-3.3-70b-versatile      │
                        └────────────────┬───────────────┘
                                         │
                        ┌────────────────▼────────────────┐
                        │            Evaluator            │
                        │    faithfulness score 0.0–1.0   │
                        └────────────────┬────────────────┘
                                         │
                 ┌───────────────────────▼──────────────────────┐
                 │                                              │
        ┌────────▼────────┐                          ┌──────────▼──────────┐
        │  Memory store   │                          │   CHAT-LOGS.json    │
        │  last 5 messages│                          │   full audit trail  │
        └─────────────────┘                          └─────────────────────┘
```

---

## Files Built on Day 5

```
src/
├── memory/
│   └── memory_store.py       ← stores last 5 messages in JSON
├── evaluation/
│   └── rag_eval.py           ← faithfulness scoring via Groq
├── deployment/
│   ├── app.py                ← main backend — all 3 endpoints
│   └── streamlit_app.py      ← Streamlit UI
└── logs/
    └── CHAT-LOGS.json        ← auto-created, logs every interaction
```

---

## The Three Endpoints

### /ask — Document QA
```
Input:  plain English question
Flow:   hybrid retrieval → rerank → Groq LLM → faithfulness score
Output: answer + sources + faithfulness score + hallucination risk
```

### /ask-image — Image QA
```
Input:  text description of image
Flow:   CLIP text embed → FAISS search → top 3 images → Groq LLM
Output: answer based on image captions and OCR text
```

### /ask-sql — Database QA
```
Input:  plain English question about data
Flow:   schema load → Groq SQL generation → validate → execute → summarize
Output: answer + generated SQL + raw result table
```

---

## CHAT-LOGS.json Structure

Every interaction is logged automatically:

```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "type": "ask",
    "question": "What are Crombie's pension benefits?",
    "answer": "Crombie has defined benefit and contribution plans...",
    "sources": [
      {"source": "text_document_1.pdf", "page": 115, "score": 7.36}
    ],
    "faithfulness": 0.91,
    "hallucination_risk": "low"
  },
  {
    "timestamp": "2024-01-15T10:31:00",
    "type": "ask-sql",
    "question": "How many customers are there?",
    "sql": "SELECT COUNT(*) FROM customers",
    "answer": "There are 10,000 customers in total.",
    "error": null
  },
  {
    "timestamp": "2024-01-15T10:32:00",
    "type": "ask-image",
    "question": "correlation matrix heatmap",
    "answer": "The image shows a correlation matrix...",
    "images": ["correlation_matrix.png"]
  }
]
```

---

## How to Run the Complete Project (Day 1 to Day 5)

### One time setup

```bash
# go to project root
cd /home/aadityasharma/Desktop/Aaditya_Sharma_Trainee_Hestabit/Week_7

# activate virtual environment
source venv_rag/bin/activate

# set API key
export GROQ_API_KEY="your-groq-key-here"

# create __init__.py in all folders
touch src/__init__.py
touch src/deployment/__init__.py
touch src/memory/__init__.py
touch src/evaluation/__init__.py
touch src/generator/__init__.py
touch src/utils/__init__.py
touch src/pipelines/__init__.py
touch src/retriever/__init__.py
touch src/embeddings/__init__.py

# create SQLite database from CSV (run once)
python -m src.utils.create_db
```

### Day 1 — text ingestion and basic retrieval

```bash
python -m src.pipelines.ingest
python -m src.retriever.query_engine
```

### Day 2 — hybrid retrieval and reranking

```bash
python -m src.retriever.hybrid_retriever
python -m src.retriever.reranker
python -m src.pipelines.context_builder
```

### Day 3 — image RAG

```bash
python -m src.embeddings.clip_embedder
python -m src.pipelines.image_ingest
python -m src.retriever.image_search
```

### Day 4 — SQL question answering

```bash
python -m src.utils.schema_loader
python -m src.generator.sql_generator
python -m src.pipelines.sql_pipeline
```

### Day 5 — memory, evaluation and Streamlit UI

```bash
# test memory
python -m src.memory.memory_store

# test evaluator
python -m src.evaluation.rag_eval

# test all three endpoints
python -m src.deployment.app

# launch Streamlit UI
python -m streamlit run src/deployment/streamlit_app.py
```

### All commands together

```bash
cd /home/aadityasharma/Desktop/Aaditya_Sharma_Trainee_Hestabit/Week_7
source venv_rag/bin/activate
export GROQ_API_KEY="your-groq-key-here"

python -m src.utils.create_db

python -m src.pipelines.ingest

python -m src.retriever.hybrid_retriever
python -m src.retriever.reranker
python -m src.pipelines.context_builder

python -m src.embeddings.clip_embedder
python -m src.pipelines.image_ingest
python -m src.retriever.image_search

python -m src.utils.schema_loader
python -m src.generator.sql_generator
python -m src.pipelines.sql_pipeline

python -m src.memory.memory_store
python -m src.evaluation.rag_eval
python -m src.deployment.app
python -m streamlit run src/deployment/streamlit_app.py
```

---


## Week 7 Completion 

| Requirement | Built | Tested |
|---|---|---|
| Text RAG end-to-end | Yes | Yes |
| Hybrid retrieval (BM25 + semantic) | Yes | Yes |
| Reranking (cross-encoder) | Yes | Yes |
| Image RAG (CLIP + OCR + BLIP) | Yes | Yes |
| SQL QA (NL → SQL → answer) | Yes | Yes |
| Conversational memory | Yes | Yes |
| Faithfulness evaluation | Yes | Yes |
| Chat logging | Yes | Yes |
| Streamlit UI | Yes | Yes |
| Works with Groq API | Yes | Yes |
| FAISS vector database | Yes | Yes |
| Documentation | Yes | Yes |
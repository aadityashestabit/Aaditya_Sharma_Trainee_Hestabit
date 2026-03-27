# Retrieval Strategies — Day 2

## The Problem with Day 1

Day 1 retrieval only used semantic search — it found chunks based on *meaning*. That works well most of the time, but it misses exact keywords. For example, searching "Crombie pension" might miss a chunk that literally contains those words but is phrased differently in vector space.

Day 2 fixes this by combining two search methods and then running a smarter final check.

---

## What We Built

### 1. BM25 Keyword Search
BM25 is the same algorithm Google used before neural search. It counts how often your query words appear in each chunk and ranks by that frequency. It's dumb but fast, and catches exact matches that semantic search misses.

### 2. Hybrid Search (BM25 + Semantic)
We run both searches and blend their scores:
```
hybrid score = (0.6 × semantic score) + (0.4 × BM25 score)
```
Semantic gets more weight because meaning matters more than keywords — but BM25 still contributes enough to rescue exact matches.

### 3. Reranker
After hybrid search returns 10 candidates, the reranker reads each (query, chunk) pair together using a cross-encoder model. It's slower but much smarter — it actually understands the relationship between the question and the chunk, not just their individual vectors.

The model used: `cross-encoder/ms-marco-MiniLM-L-6-v2`

### 4. Deduplication
If two chunks come from the same page, only the higher-scoring one is kept. No point sending the LLM the same page twice.

---

## The Full Flow

```
User query
    ↓
Semantic search → top 10 candidates
BM25 search     → top 10 candidates
    ↓
Merge + blend scores (hybrid)
    ↓
Reranker picks best 5
    ↓
Deduplicate by page
    ↓
Clean context string → ready for LLM
```

---

## Real Results from Our Test

Query: *"What are Crombie's pension benefits?"*

| Stage | Top result score | Notes |
|---|---|---|
| Semantic only (Day 1) | 0.57 | Good but misses keyword hits |
| Hybrid | 0.74 | BM25 boosted the best chunk to 1.0 |
| After reranking | 7.36 | Promoted a chunk hybrid ranked 6th |

The reranker promoted a chunk with hybrid score 0.30 all the way to position 2 — it would have been completely missed by Day 1 retrieval.

---

## Files

```
retriever/
├── hybrid_retriever.py   # BM25 + semantic fusion
├── reranker.py           # Cross-encoder reranking
pipelines/
└── context_builder.py    # Full pipeline: retrieve → rerank → dedupe → format
```

---

## Key Takeaway

Day 1 retrieval is like a librarian who browses by topic. Day 2 is that same librarian, but now with a keyword index AND the ability to skim each book before handing it to you. The results are noticeably better — and that directly reduces hallucination in the final LLM answer.
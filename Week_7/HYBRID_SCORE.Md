# Hybrid Score Fusion — Semantic + BM25

## The Core Problem

Semantic search and BM25 are good at different things:

- **Semantic search** understands *meaning* — "pension plan" matches "retirement benefits" even though the words are different
- **BM25** understands *keywords* — "Crombie" matches "Crombie" exactly, no guessing

Neither one alone is enough. Combining them gives you the best of both worlds.

---

## The Theory

### What is BM25?
BM25 (Best Match 25) is a classical keyword ranking algorithm. It scores a chunk based on how often your query words appear in it, adjusted for chunk length. A chunk that contains "pension" 5 times scores higher than one that contains it once. It has no understanding of meaning — just word frequency.

### What is Semantic Search?
Semantic search converts both the query and chunks into vectors using an embedding model. Chunks with similar *meaning* end up close together in vector space. It understands that "retirement plan" and "pension benefits" are the same concept — but may miss exact keyword matches.

### Why combine them?
Each method has blind spots:

| Situation | Semantic | BM25 |
|---|---|---|
| "pension" → "retirement plan" | Finds it | Misses it |
| Exact company name "Crombie" | May miss it | Finds it |
| Specific number "48.84 Mbps" | May miss it | Finds it |
| Vague question "what about benefits" | Finds it | Misses it |

Combining both means neither blind spot affects your final result.

---

## The Flow

```
User query: "What are Crombie's pension benefits?"
                        │
          ┌─────────────┴──────────────┐
          │                            │
          ▼                            ▼
  ┌───────────────┐           ┌─────────────────┐
  │ Embed query   │           │ Tokenize query  │
  │ (MiniLM)      │           │ (split words)   │
  └───────┬───────┘           └────────┬────────┘
          │                            │
          ▼                            ▼
  ┌───────────────┐           ┌─────────────────┐
  │ FAISS search  │           │  BM25 scoring   │
  │ (vector sim)  │           │ (word frequency)│
  └───────┬───────┘           └────────┬────────┘
          │                            │
          ▼                            ▼
  ┌───────────────┐           ┌─────────────────┐
  │ L2 distance   │           │ Normalize by    │
  │ → 0-1 score   │           │ max BM25 score  │
  │ 1/(1+dist)    │           │ score/max_score │
  └───────┬───────┘           └────────┬────────┘
          │  semantic_score            │  bm25_score
          │  range: 0 to 1             │  range: 0 to 1
          └─────────────┬──────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Weighted Average    │
            │                       │
            │  hybrid = (0.6 × sem) │
            │        + (0.4 × bm25) │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Sort by hybrid score │
            │  Return top 10        │
            └───────────┬───────────┘
                        │
                        ▼
                  Reranker (Day 2)
```

---

## Score Normalization — Why It Matters

Before combining, both scores must live in the same range (0 to 1). Without normalization, BM25 raw scores can be 0 to 15+ while FAISS distances are 0 to 2 — adding them directly would be meaningless.

### Semantic score conversion
```python
# FAISS returns L2 distance (lower = more similar)
# Convert to similarity score (higher = more similar)
semantic_score = 1 / (1 + distance)

# Examples:
# distance = 0.0  →  score = 1.00  (perfect match)
# distance = 0.5  →  score = 0.67
# distance = 1.0  →  score = 0.50
# distance = 2.0  →  score = 0.33
```

### BM25 score normalization
```python
# BM25 returns raw frequency scores (e.g. 0 to 12.4)
# Normalize so the best result always = 1.0
bm25_score = raw_score / max_score

# Examples (if max raw score is 8.2):
# raw = 8.2  →  score = 1.00  (top keyword match)
# raw = 4.1  →  score = 0.50
# raw = 0.0  →  score = 0.00  (word not found)
```

---

## The Combination Code

No external library. Pure Python math:

```python
hybrid_score = (semantic_weight * sem_score) + (bm25_weight * bm25_score)

# Default weights
semantic_weight = 0.6
bm25_weight     = 0.4
```

---

## Real Example From Our Test

Query: *"What are Crombie's pension benefits?"*

```
Chunk: p.115 — "9) EMPLOYEE FUTURE BENEFITS..."

  Semantic score : 0.57  ×  0.6  =  0.342
  BM25 score     : 1.00  ×  0.4  =  0.400
                              ─────────────
  Hybrid score   :             =  0.742  → Ranked 1st


Chunk: p.116 — "Information about Crombie's defined benefit plans..."

  Semantic score : 0.55  ×  0.6  =  0.330
  BM25 score     : 0.54  ×  0.4  =  0.216
                              ─────────────
  Hybrid score   :             =  0.546  → Ranked 2nd
```

p.115 won because it had a perfect BM25 score of 1.0 — it contained the most exact keyword matches. Semantic alone would have ranked it lower at 0.57.

---

## Tuning the Weights

The 60/40 split is a good default but can be adjusted:

| Document type | Recommended weights |
|---|---|
| General enterprise docs | Semantic 0.6 / BM25 0.4 |
| Legal contracts (keyword-heavy) | Semantic 0.5 / BM25 0.5 |
| Conversational / narrative docs | Semantic 0.7 / BM25 0.3 |
| Technical docs with exact terms | Semantic 0.4 / BM25 0.6 |

---

## Summary

| Component | Library | Purpose |
|---|---|---|
| Semantic search | `faiss-cpu` + `sentence-transformers` | Meaning-based similarity |
| BM25 search | `rank_bm25` | Keyword frequency matching |
| Score normalization | Pure Python | Bring both to 0–1 range |
| Score combination | Pure Python math | Weighted average |

The combination itself is just one line of math — the intelligence comes from normalizing both scores correctly before adding them.
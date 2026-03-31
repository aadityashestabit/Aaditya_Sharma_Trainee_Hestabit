import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

try:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except:
    model = None

def faithfulness_score(answer, context):
    try:
        context_texts = [c["text"] for c in context if c.get("text", "").strip()]
        if not context_texts or not answer.strip():
            return 0.5
    except:
        return 0.5

    try:
        context_emb = model.encode(context_texts) if model is not None else []
        answer_emb  = model.encode(answer) if model is not None else []
        similarities = cosine_similarity([answer_emb], context_emb)[0]
        return float(similarities.max())
    except:
        return 0.5

def confidence_score(score):
    try:
        return round(min(max(score, 0.0), 1.0), 2)
    except:
        return 0.5

def hallucination_risk(score):
    try:
        if score >= 0.75: return "LOW"
        if score >= 0.5:  return "MEDIUM"
        return "HIGH"
    except:
        return "MEDIUM"

def evaluate(answer, context):
    try:
        if not context or not answer.strip():
            return {
                "faithfulness":       0.5,
                "confidence":         0.5,
                "hallucination_risk": "MEDIUM"
            }
    except:
        return {
            "faithfulness":       0.5,
            "confidence":         0.5,
            "hallucination_risk": "MEDIUM"
        }

    try:
        faith = faithfulness_score(answer, context)
        return {
            "faithfulness":       faith,
            "confidence":         confidence_score(faith),
            "hallucination_risk": hallucination_risk(faith)
        }
    except:
        return {
            "faithfulness":       0.5,
            "confidence":         0.5,
            "hallucination_risk": "MEDIUM"
        }

def refine_answer(draft_answer, context):
    try:
        if not context:
            return draft_answer
    except:
        return draft_answer

    try:
        score = faithfulness_score(draft_answer, context)
        if score < 0.35:
            return "Based on the available context, there is insufficient information to answer this question reliably."
        return draft_answer
    except:
        return draft_answer
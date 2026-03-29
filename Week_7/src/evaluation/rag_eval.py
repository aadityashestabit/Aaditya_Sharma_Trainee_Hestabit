import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

def score_faithfulness(question, context, answer):
    prompt = f"""You are a RAG evaluation expert. Score how faithful the answer is to the given context.

QUESTION: {question}

CONTEXT (retrieved documents):
{context[:1500]}

ANSWER:
{answer}

Rate the faithfulness from 0.0 to 1.0 where:
1.0 = answer is completely grounded in the context
0.5 = answer is partially grounded, some unsupported claims
0.0 = answer is completely hallucinated, not in context at all

Reply with ONLY a number between 0.0 and 1.0. Nothing else."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    try:
        score = float(raw)
        return round(min(max(score, 0.0), 1.0), 2)
    except:
        return 0.5  # default if parsing fails

def detect_hallucination(score):
    if score >= 0.8:
        return "low"        # answer is faithful
    elif score >= 0.5:
        return "medium"     # some unsupported claims
    else:
        return "high"       # likely hallucinated

if __name__ == "__main__":
    question = "What are Crombie's pension benefits?"
    context  = "Crombie has defined benefit and contribution plans for pension..."
    answer   = "Crombie offers pension plans including defined benefit plans."
    score    = score_faithfulness(question, context, answer)
    print(f"Faithfulness score: {score}")
    print(f"Hallucination risk: {detect_hallucination(score)}")
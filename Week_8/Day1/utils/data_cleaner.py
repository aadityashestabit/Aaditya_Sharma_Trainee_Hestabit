import json, re, random

MIN_INSTRUCTION_LEN = 10
MIN_OUTPUT_LEN      = 20
MAX_OUTPUT_LEN      = 500

def clean_text(text):
    """Remove HTML tags, weird chars, extra spaces."""
    if not text: return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^\w\s\.,!?;:()\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_sample_type(text):
    """Decide type by reading actual question content."""
    t = text.lower()
    reasoning  = ["why", "explain", "how does", "what causes",
                  "mechanism", "reason", "difference between", "compare"]
    extraction = ["what medications", "list", "identify", "extract",
                  "what are the symptoms", "how long", "duration", "dosage"]
    if   any(k in t for k in reasoning):  return "reasoning"
    elif any(k in t for k in extraction): return "extraction"
    else: return "qa"

def format_sample(row, sample_type="qa"):
    """Convert raw row into instruction/input/output format."""
    instructions = {
        "qa":        "Answer the following medical question as a helpful doctor.",
        "reasoning": "Think step by step and explain your reasoning, then answer the following medical question.",
        "extraction":"Read the patient message and extract: (1) main symptom, (2) duration if mentioned, (3) any medications mentioned."
    }
    return {
        "instruction": instructions.get(sample_type, "Answer the following medical question."),
        "input":       clean_text(row["input"]),
        "output":      clean_text(row["output"])
    }

def is_valid_sample(sample):
    """Return True only if sample meets quality thresholds."""
    inst = sample.get("instruction", "")
    out  = sample.get("output", "")
    if not inst or not out:                           return False
    if len(inst) < MIN_INSTRUCTION_LEN:                return False
    if len(out) < MIN_OUTPUT_LEN or len(out) > MAX_OUTPUT_LEN: return False
    return True

def remove_duplicates(samples):
    """Remove rows where instruction + input is identical."""
    seen, deduped = set(), []
    for s in samples:
        key = s["instruction"] + s["input"]
        if key not in seen:
            seen.add(key)
            deduped.append(s)
    print(f"Removed {len(samples)-len(deduped)} duplicates. Kept {len(deduped)}")
    return deduped

def save_jsonl(samples, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for s in samples:
                f.write(json.dumps(s, ensure_ascii=False) + '\n')
        print(f"Saved {len(samples)} → {filepath}")
    except Exception as e: print(f" Error: {e}")

def load_jsonl(filepath):
    samples = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip(): samples.append(json.loads(line.strip()))
    except Exception as e: print(f" Error: {e}")
    return samples

print(' All helper functions ready')
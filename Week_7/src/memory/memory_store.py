import json
import os

MEMORY_FILE = "src/memory/chat_memory.json"
MAX_MESSAGES = 5

os.makedirs("src/memory", exist_ok=True)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def add_message(role, content):
    messages = load_memory()
    messages.append({"role": role, "content": content})
    # keep only last 5 messages
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]
    save_memory(messages)

def get_memory():
    return load_memory()

def clear_memory():
    save_memory([])
    print("Memory cleared.")

if __name__ == "__main__":
    clear_memory()
    add_message("user", "How much download speed for work from home ")
    add_message("assistant", "Crombie has defined benefit and contribution plans...")
    add_message("user", "What about the post employment benefits?")
    print("Current memory:")
    for m in get_memory():
        print(f"  [{m['role']}]: {m['content'][:60]}")
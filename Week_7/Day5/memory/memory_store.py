import json
import os

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_FILE   = os.path.join(BASE_DIR, "src", "memory", "chat_memory.json")
CHAT_LOG_FILE = os.path.join(BASE_DIR, "src", "logs", "CHAT-LOGS.json")
MAX_MESSAGES = 5

try:
    os.makedirs("src/memory", exist_ok=True)
except:
    pass

def load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            return []
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(messages):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(messages, f, indent=2)
    except:
        pass

def add_message(role, content):
    try:
        messages = load_memory()
        messages.append({"role": role, "content": content})

        if len(messages) > MAX_MESSAGES:
            messages = messages[-MAX_MESSAGES:]

        save_memory(messages)
    except:
        pass

def get_memory():
    try:
        return load_memory()
    except:
        return []

def clear_memory():
    try:
        save_memory([])
        print("Memory cleared.")
    except:
        pass

if __name__ == "__main__":
    try:
        clear_memory()
        add_message("user", "How much download speed for work from home ")
        add_message("assistant", "Crombie has defined benefit and contribution plans...")
        add_message("user", "What about the post employment benefits?")
        print("Current memory:")
        for m in get_memory():
            print(f"  [{m['role']}]: {m['content'][:60]}")
    except:
        pass
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen_core.models import SystemMessage, UserMessage
from loader import LLMclient
from memory.session_memory import SessionMemory
from memory.vector_store import FaissVectorStore


def build_memory_context(recent: str, facts: str, vectors: str) -> str:
    return (
        "Relevant memory context:\n\n"
        f"Short-term session memory:\n{recent}\n\n"
        f"Long-term facts:\n{facts}\n\n"
        f"Vector recall:\n{vectors}\n"
    )


async def main():
    os.makedirs("memory", exist_ok=True)

    model_client = LLMclient().llmclient

    session = SessionMemory(
        db_path="memory/long_term.db",
        max_turns=10
    )
    vector_store = FaissVectorStore(
        index_path="memory/vector.index",
        metadata_path="memory/vector_metadata.pkl",
    )

    print("\n=== Day 4: Memory-Aware Agent ===")
    print(f"  Short-term : sliding window (last 10 turns)")
    print(f"  Long-term  : SQLite facts  (memory/long_term.db)")
    print(f"  Vector     : FAISS index   ({vector_store.total_vectors} vectors loaded)")
    print("  Type 'exit' to quit.\n")

    while True:
        try:
            user_query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Shutting down]")
            break

        if not user_query:
            continue
        if user_query.lower() in ("exit", "quit"):
            break

        # step 1 — retrieve from all 3 memory stores before generating
        fact_hits   = session.search_facts(user_query, limit=5)
        vector_hits = vector_store.search(user_query, k=3)

        recent_context = session.format_recent_context()
        fact_context   = session.format_fact_results(fact_hits)
        vector_context = vector_store.format_search_results(vector_hits)

        memory_context = build_memory_context(recent_context, fact_context, vector_context)

        # step 2 — inject memory context into the prompt
        system_prompt = (
            "You are a memory-aware assistant. "
            "Use the retrieved memory context when it is relevant to the user's query. "
            "Do not invent past context that isn't there. "
            "Answer naturally and clearly. Plain text only."
        )

        user_prompt = (
            f"{memory_context}\n\n"
            f"Current query:\n{user_query}"
        )

        # step 3 — generate response
        try:
            result = await model_client.create([
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt, source="user"),
            ])
            answer = str(result.content).strip()
        except Exception as e:
            print(f"[Error] Model call failed: {e}")
            continue

        # step 4 — show memory retrieval + answer
        print("\n---- MEMORY RETRIEVAL ----")
        print(memory_context)
        print("---- ASSISTANT ANSWER ----")
        print(answer)
        print()

        # step 5 — store this turn back into all memory stores
        session.add_turn("user", user_query)
        session.add_turn("assistant", answer)

        # extract and persist any important facts from both sides
        user_facts      = session.extract_important_facts(user_query)
        assistant_facts = session.extract_important_facts(answer)
        session.store_facts(user_facts + assistant_facts)

        # add to vector store for future semantic search
        vector_store.add_text(user_query, {"role": "user"})
        vector_store.add_text(answer,     {"role": "assistant"})


if __name__ == "__main__":
    asyncio.run(main())
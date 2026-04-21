## The Problem with Stateless Agents

Every agent we built in Days 1 through 3 starts fresh every time. You tell it your name, it acknowledges it, you close the terminal, you open it again, and it has no idea who you are. It is not being rude — it genuinely has no way to remember. Each run is a completely isolated event with no connection to any previous run.

For a simple question-answering tool this is fine. For anything that feels like a real assistant it is a fundamental limitation. A useful assistant remembers context. It builds on previous conversations. It knows things about you without you having to repeat them every session.

Day 4 fixes this. We build a memory system that gives the agent three different kinds of memory, each capturing a different type of context at a different time scale. Together they make the agent feel like something that actually knows you.

---

## Why Three Layers?

You might wonder why not just store everything in one place and search it. The answer is that different kinds of memory work differently and serve different purposes.

Some context is only relevant right now — the last few things you said in the current conversation. Keeping this forever would be wasteful, and you would not want it to come back up months later.

Some context is important enough to remember forever — your name, where you work, what you are building. This needs to be stored permanently and found reliably even if you used completely different words to ask about it.

Some context is relevant by topic rather than by exact words — a conversation you had two weeks ago about machine learning might be relevant when you ask about transformers today, even though neither message mentioned the other. Finding this kind of connection requires something smarter than keyword matching.

Three layers, three different problems, three different solutions.

---

## Short-Term Memory — The Sliding Window

Short-term memory holds the current conversation. It uses a sliding window that keeps the last ten exchanges and automatically drops older ones as new ones arrive.

Think of it like the working memory you use when someone is talking to you. You do not remember every word anyone has ever said to you, but you do hold the last few sentences of the current conversation in your head so you can follow along and respond coherently. That is exactly what this layer does.

When you ask a follow-up question like "what did you mean by that?" the agent knows what "that" refers to because the recent exchanges are still in context. Without this layer every message would be treated as if it arrived in a vacuum with no prior conversation.

This memory is intentionally lost when the session ends. It is not a bug — ephemeral context should be ephemeral.

---

## Long-Term Memory — SQLite Facts

Long-term memory stores important facts permanently in a SQLite database file on disk. These facts survive restarts. Close the terminal, open it again a week later, ask "what is my name?" — the agent will know.

Not everything gets stored. The system scans messages for patterns that suggest persistent personal information — things like "my name is", "I work at", "I like", "I prefer". Only these get written to the database. Casual conversation and transient context are not persisted. The goal is to capture the kind of facts you would want any assistant to remember long-term without filling the database with noise.

When a new query comes in, the database is searched for facts that share words with the query. This is keyword-based retrieval — simple but effective for the kind of factual personal information we are storing. If you ask "where do I work" it finds the fact "I work at Hestabit Technologies" because both contain the word "work".

---

## Vector Memory — FAISS Semantic Search

Vector memory is the most powerful of the three layers and the hardest to explain without going into how language models work.

Every piece of text — every sentence, every paragraph — can be converted into a list of numbers called an embedding. These numbers capture the meaning of the text in a mathematical space. Two sentences that mean similar things end up as similar lists of numbers, even if they use completely different words. "I enjoy building AI systems" and "I like working on machine learning projects" are about the same topic even though they share almost no words. Their embeddings would be numerically close.

FAISS (Facebook AI Similarity Search) is a library that stores these embeddings and finds the closest ones to any new query extremely efficiently. Every user message and every assistant response gets embedded and stored. When a new query comes in it gets embedded and compared against everything stored. The closest matches come back as related context.

This is what makes the system feel genuinely intelligent about memory. You ask about neural networks and it surfaces a conversation you had about deep learning three sessions ago, even though you never mentioned either in the current message.

---

## The Retrieve-Inject-Generate-Store Loop

The entire memory system works through a single loop that runs on every query. Understanding this loop is the key to understanding how the agent appears to remember things.

Before the model generates anything, the system searches all three memory stores and collects everything relevant. The recent conversation, the matching long-term facts, the semantically similar past exchanges — all of it gets formatted into a memory context block. That block gets injected into the prompt as text before the user query.

The model does not have memory in any special sense. It is just reading text that was given to it. The intelligence is not in the model — it is in what you put in front of it. Retrieval-augmented memory, just like RAG for documents, is about engineering the prompt so that the model appears to remember.

After the model generates its response, the new exchange gets stored back into all three layers. The conversation turn goes into short-term memory. Any important facts get extracted and stored in SQLite. Both the user message and the response get embedded and added to the FAISS index. The index and database are saved to disk immediately so nothing is lost if the program closes.

---

## Execution Flow Diagram

```
User types a query
    |
    v
[Memory Retrieval — searches all 3 stores simultaneously]
  ├── Short-term:  last 10 turns from current session deque
  ├── Long-term:   keyword search in SQLite facts database
  └── Vector:      semantic search in FAISS index (top 3 matches)
    |
    v
[Memory Context Built]
  "Recent conversation: ..."
  "Relevant facts: My name is Aaditya, I work at Hestabit..."
  "Related past context: [previous exchange about AI agents]"
    |
    v
[Prompt Assembled]
  memory context + current query → sent to model
    |
    v
[Model Generates Response]
  has full context of who you are and what was discussed before
    |
    v
[Response shown to user]
    |
    v
[Memory Storage — updates all 3 stores]
  ├── Short-term:  add this turn to session deque
  ├── Long-term:   extract important facts → write to SQLite
  └── Vector:      embed query + response → add to FAISS index
                   save index to disk immediately
    |
    v
Ready for next query
(FAISS index and SQLite persist across sessions)
```

---

## File Structure

```
Day4/
├── memory/
│   ├── session_memory.py    ← short-term deque + long-term SQLite facts
│   └── vector_store.py      ← FAISS semantic search with sentence-transformers
├── loader.py                ← LLM client
├── run_day4.py              ← main memory-aware chat loop
└── MEMORY-SYSTEM.md         ← this file
```

---


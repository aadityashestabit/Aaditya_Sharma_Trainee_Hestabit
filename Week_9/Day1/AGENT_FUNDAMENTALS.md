# Day 1 — Agent Foundations & Message-Based Communication

## What is an AI Agent?

Before we get into code, it helps to understand what makes something an "agent" versus just a chatbot or a script.

A chatbot responds to messages. A script executes fixed steps. An agent does something more interesting — it perceives its environment, reasons about what it received, and takes an action. That action could be generating text, calling a tool, or passing information to another agent.

The core loop every agent runs is:

```
Perception → Reasoning → Action
```

In our case:
- **Perception** is reading the input (user query or previous agent output)
- **Reasoning** is what the LLM does with the system prompt and input
- **Action** is the text output that gets passed forward

---

## Agent vs Chatbot vs Pipeline

These three things are often confused but they're meaningfully different.

A **chatbot** is a single model that responds to whatever you send it. It has no fixed role, no specialization, and usually no persistent memory. You ask it anything, it answers.

A **pipeline** is a fixed sequence of functions. Data goes in one end, comes out the other. Every run follows the same path regardless of the input. No intelligence in the routing.

An **agent** has a defined role, follows constraints set by its system prompt, can have memory, and its output is meaningful to the next step in a larger system. It's not just responding — it's performing a specific job.

Our Day 1 builds a **pipeline of agents** — three agents with strict roles chained in a fixed order. This is the simplest form of multi-agent architecture and the right place to start before adding orchestration and dynamic routing.

---

## Role Isolation

The most important concept in Day 1 is role isolation. Each agent knows exactly what its job is and — equally important — what its job is NOT.

The Research Agent gathers facts. It must not summarize them. It must not give a final answer. The Summarizer compresses. It must not answer the user directly. The Answer Agent writes the final response. It must not mention that it received a summary from another agent.

This is enforced entirely through the system prompt:

```python
# Research Agent
"Do NOT summarize. Do NOT give a final answer. Do NOT give advice."

# Summarizer Agent  
"Do NOT answer the user's question directly. Do NOT give recommendations."

# Answer Agent
"Do NOT mention summaries or other agents. Answer naturally."
```

If you remove these constraints the agents start bleeding into each other's roles and the output quality drops. The system prompt IS the agent's identity — it defines what the agent is and what it refuses to do.

---

## ReAct Pattern

ReAct stands for Reason + Act. It's a prompting pattern where the model is instructed to think step by step before taking action.

In a ReAct agent the model produces:
1. A Thought — what it understands about the problem
2. An Action — what it's going to do next
3. An Observation — what it got back
4. A Final answer based on those observations

We saw this pattern show up uninvited in Day 1 — some Groq models were trained on so much ReAct data that they started producing Thought/Action/Observation format even when we didn't ask for it. The fix was adding "Do NOT use Thought/Action/Observation format" to the system prompt and switching to a model that doesn't force this behavior.

---

## Memory Window

Every agent in Day 1 has a memory window of 10. This is set using AutoGen's `BufferedChatCompletionContext`:

```python
model_context=BufferedChatCompletionContext(buffer_size=10)
```

Without a memory window, every message in the conversation gets added to the context that gets sent to the model. After 50 or 100 turns this becomes enormous, hits token limits, and either crashes or becomes very slow.

The buffer size of 10 means only the last 10 messages are kept. Older messages are automatically dropped. This is implemented using Python's `deque(maxlen=10)` internally — a data structure that automatically removes the oldest item when a new one is added and it's already at capacity.

For Day 1 the memory window doesn't matter much since each agent only gets called once per query. It becomes critical in Day 4 when agents have ongoing conversations.

---

## How the Chain Works

The three agents are chained sequentially. Each agent's output becomes the next agent's input:

```
User types a question
    ↓
Research Agent receives the raw question
    ↓ outputs detailed bullet-point facts
Summarizer Agent receives those facts
    ↓ outputs a compressed 4-6 sentence summary
Answer Agent receives the summary AND the original question
    ↓ outputs the final answer the user sees
```

The Answer Agent receives both the summary and the original question. This is important. If it only gets the summary it doesn't know what was asked and produces a confused or generic answer — we saw this happen in testing

---

## Why Factory Functions

The agents are defined inside `get_research_agent()` functions rather than directly at module level. This is not just style — there's a real technical reason.

When Python imports a module it executes the top-level code immediately. If you create an AutoGen agent at the top level of a file, it gets created before any async event loop exists. The first `asyncio.run()` call creates a new event loop but the agent was already born outside it. This mismatch causes the first call to return empty output.

By wrapping agent creation in a function and calling that function from inside the async pipeline, the agent is always created within the event loop's lifetime. The problem disappears.

```python
# causes blank output on first run
research_agent = AssistantAgent(...)  # created at import time

# works correctly every time
def get_research_agent():
    return AssistantAgent(...)        # created when called, inside event loop
```

---

## What We Used

- **AutoGen** (`autogen-agentchat`) — the agent framework that handles message passing, context management, and the `.run()` interface
- **Groq API** — free LLM API endpoint, compatible with OpenAI format
- **`llama-3.1-8b-instant`** — the model that works reliably without forcing tool calls or ReAct format
- **`OpenAIChatCompletionClient`** — AutoGen's client that talks to any OpenAI-compatible API including Groq

---

## Files

```
Day1/
├── agents/
│   ├── research_agent.py   
│   ├── summarizer_agent.py  
│   └── answer_agent.py       
├── loader.py                 
├── run_pipeline.py            
└── AGENT-FUNDAMENTALS.md     
```
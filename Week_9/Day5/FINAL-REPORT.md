## Week 9 — Agentic AI & Multi-Agent System Design

---

## Executive Summary

This report documents the complete work done across Week 9 of the Hestabit AI training program. The objective was to build a progression of increasingly capable AI systems — starting from single agents, moving through multi-agent orchestration, tool use, and memory, and culminating in a fully autonomous multi-agent system called Nexus AI.

Every deliverable was built from scratch using Microsoft AutoGen, Groq's free API tier, and open-source tools. No paid APIs beyond Groq were used. All systems run fully locally or on free-tier cloud endpoints. By the end of the week the result is a production-grade autonomous AI system capable of planning, researching, coding, analyzing, self-reflecting, and delivering polished outputs — all without human intervention beyond the initial prompt.

---

## What Was Built Each Day

### Day 1 — Agent Foundations

The week began with the most fundamental question: what actually makes something an agent rather than just a chatbot or a script? An agent has a defined role, follows behavioral constraints set by its system prompt, maintains memory within a session, and its output feeds into something larger.

Day 1 produced three agents chained together — a Research Agent that gathers raw facts, a Summarizer that compresses them, and an Answer Agent that writes the final response the user sees. Each agent was given strict role isolation through its system prompt, preventing any agent from doing another's job. The chain used AutoGen's message-passing system and a sliding window memory buffer that keeps the last ten exchanges without growing unbounded.

The key insight from Day 1 was that the system prompt is the agent's identity. Every behavioral property of an agent — what it does, what it refuses to do, how it formats output — is encoded in that prompt.

### Day 2 — Multi-Agent Orchestration

Day 1's fixed chain was replaced with a dynamic orchestration system. A Planner reads the user query and generates a structured execution plan using Pydantic schema validation. The plan is a DAG — a graph of tasks where some can run in parallel and others must wait for earlier tasks to finish.

The DAG executor finds all tasks with no unmet dependencies and runs them simultaneously. As tasks complete, newly unblocked tasks start. A semaphore limits concurrent execution to prevent rate limit errors on the free API tier. A Reflection Agent reviews the final output and a Validator checks it against the original query before anything reaches the user.

The shift from Day 1 to Day 2 is the shift from pipelines to orchestration. The query determines the plan. Simple questions get small plans. Complex tasks get large ones with parallel workers.

### Day 3 — Tool-Calling Agents

Until Day 3 every agent only generated text. Day 3 gave agents the ability to take real actions. Three specialist agents were built — a FILE agent that reads and writes actual files on disk, a DB agent that creates and queries real SQLite databases, and a CODE agent that writes and executes Python in a subprocess.

The CODE agent includes auto-install functionality that detects missing packages from import statements and installs them before running the code. This makes it self-sufficient — it handles its own dependencies without any manual setup.

Two separate model clients were introduced here for the first time. The Planner uses a smaller fast model for JSON plan generation. The tool agents use a larger model that reliably generates correct function call format.

### Day 4 — Memory Systems

Day 4 gave the agent persistent memory across sessions. Three memory layers work together. Short-term memory holds the current conversation in a sliding window. Long-term memory stores important personal facts in a SQLite database that survives restarts. Vector memory stores semantic embeddings of every exchange using FAISS and finds related past conversations by meaning rather than keyword.

The core pattern is retrieve-inject-generate-store. Before every response the system searches all three memory stores and injects relevant context into the prompt. After every response the new exchange is stored back into all three layers. The model itself has no special memory capability — retrieval-augmented memory is entirely about what you put in the prompt.

### Day 5 — Nexus AI (Capstone)

Day 5 combines everything into Nexus AI — a nine-agent autonomous system with dynamic agent spawning, persistent memory, self-reflection loops, tool use, logging, failure recovery, and a Streamlit dashboard.

The nine agents cover the full lifecycle of complex reasoning work: Orchestrator, Planner, Researcher, Coder, Analyst, Critic, Optimizer, Validator, and Reporter. The Orchestrator decides which agents are needed for any given query. A simple question might use one. A complex research task might use seven. Nothing is hardcoded.

The self-reflection loop — Critic reviews output, Optimizer improves it, Validator confirms the improvement addressed the right things — is what separates Nexus AI from a simple pipeline. The system audits its own work before delivering it.

---

## Technical Stack

All systems were built on a consistent technical foundation throughout the week.

AutoGen from Microsoft provided the agent framework — message passing, context management, tool registration, and the AssistantAgent abstraction. Groq's free API tier provided access to large language models without cost. The primary models used were llama-3.1-8b-instant for planning and JSON generation, and llama-4-scout-17b-16e-instruct for reasoning and tool use. FAISS from Facebook AI provided efficient vector similarity search. Sentence-transformers provided local CPU embedding generation using the all-MiniLM-L6-v2 model. SQLite provided persistent relational storage. Pydantic provided schema validation for structured agent outputs. Streamlit provided the web dashboard for Day 5.

---

## Key Concepts Demonstrated

The week demonstrated a progression of increasingly sophisticated AI engineering concepts.

Role isolation through system prompts is the foundation of reliable multi-agent behavior. An agent that tries to do everything does nothing well. Precise, constraining system prompts are what keep agents in their lanes.

Dynamic orchestration separates intelligent systems from fixed pipelines. When the plan is generated at runtime based on the query rather than hardcoded in the source, the system can handle the full range of human requests rather than just the ones its author anticipated.

Tool use is what transforms agents from text generators into systems that can act on the world. The gap between "describing what code would do" and "actually executing code and returning real output" is enormous in terms of practical usefulness.

Retrieval-augmented memory is the mechanism that makes agents feel like they know you. The model has no memory — you build it externally and inject it as context. The sophistication is in what you retrieve and how you present it.

Self-reflection loops are what separate adequate outputs from excellent ones. Having the system critique its own work and improve it before delivery catches the gaps and weaknesses that a single-pass generation would miss.

Structured outputs with Pydantic make multi-agent communication reliable. Free-form text between agents is fragile. Schema-validated JSON is robust.

---

## What was done in whole week

At the start of the week the capability was a single agent that could answer a question. At the end of the week the capability is an autonomous system that can plan a startup, design an architecture, write and execute code, analyze data, critique its own outputs, and deliver polished reports — without any human coordination between the steps.

The engineering principles that made this progression possible are not complex. Role isolation. Structured communication. Dynamic planning. Context injection. Persistent memory. Self-reflection. Each one is simple on its own. The sophistication is in understanding how they compose — how each layer enables the next and how the combination produces something that feels genuinely capable.

These are the foundations of production AI systems. The same patterns that run Nexus AI are the patterns that run commercial autonomous agents, enterprise copilots, and AI-powered workflows at scale. The specific models and frameworks will change. The underlying architecture will not.

---

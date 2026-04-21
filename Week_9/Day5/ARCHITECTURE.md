## Week 9 — Day 5: Nexus AI — Autonomous Multi-Agent System

## NEXUS AI

Every previous day added one piece to the puzzle. Day 1 showed how agents chain together. Day 2 showed how a planner can orchestrate dynamic work. Day 3 gave agents real tools to act on the world. Day 4 gave agents persistent memory. Day 5 combines all of it into a single autonomous system.

Nexus AI is not a chatbot. It does not have one fixed behavior. You give it a query and it figures out what needs to happen, decides which specialist agents are required, runs them in the right order, reflects on the output quality, validates the result, and delivers a final answer. At no point do you configure which agents run or how many steps there are. The system decides.

That is what autonomous means in this context. The intelligence is not in any single agent — it is in the architecture that coordinates them.

---

## The Nine Agents

Nexus AI has nine specialist agents, each with a precise role and detailed instructions about what it must and must not do. The separation of roles is intentional. An agent that tries to do everything does nothing well.

The Orchestrator is the entry point. It reads every query and produces a JSON execution plan listing which agents should run, in what order, and what each one should do. It knows all eight other agents and their capabilities. It picks the minimum set needed for the query — a simple question might need one agent, a complex research task might need six.

The Planner creates detailed step-by-step breakdowns for complex tasks. Not every query needs a Planner. The Orchestrator only includes it when the task genuinely requires structured upfront planning before execution can begin.

The Researcher provides deep background knowledge, frameworks, and factual context on any topic. It draws on training knowledge directly and is explicitly instructed not to fabricate statistics or certainty it does not have.

The Coder writes and executes Python. Every piece of code it generates actually runs. It handles its own package dependencies and always retries if execution fails.

The Analyst takes data or research output and produces evidence-based conclusions. It quantifies where possible, ranks insights by impact, and never states a finding without something in the provided data to support it.

The Critic reviews the previous output and finds specific weaknesses. It scores the output, lists every issue with a required improvement, and gives direct honest feedback rather than polite vagueness. Its job is to find problems, not to be encouraging.

The Optimizer takes the Critic's feedback and produces an improved version that addresses every point raised. It returns the complete improved output, not just a list of changes. After optimization the result should be measurably better than what the Critic reviewed.

The Validator does a final correctness check. It verifies the output actually answers the original query, checks for factual errors, and either passes the output through or fixes whatever is missing. It is the last line of quality control before the user sees anything.

The Reporter formats everything into a polished final document. It is only invoked when the user explicitly asks for a report or document — never automatically. It produces structured output with standard sections: executive summary, key findings, detailed analysis, recommendations, and next steps.

---

## Dynamic Agent Spawning

The most important architectural decision in Nexus AI is that agent selection is completely dynamic. The Orchestrator reads the query and decides what is needed. Nothing is hardcoded.

A question like "what is a transformer architecture" needs one agent — the Researcher. There is no value in running an Analyst, Critic, Optimizer, Validator, and Reporter on a simple explanation. That would be slow and wasteful.

A task like "plan a healthcare AI startup and produce a detailed report" needs most of the roster — Research to understand the space, Analysis to identify opportunities, Critic and Optimizer to improve the quality, Validator to check completeness, and Reporter to format the final document.

The system scales with the complexity of the request. Simple stays simple. Complex gets the full treatment.

---

## Output Chaining

Every agent in the pipeline receives the accumulated outputs of all agents that ran before it. This is the same context injection mechanism from Day 3 but applied at the full multi-agent level.

The Analyst does not just receive its own task. It receives its task plus everything the Researcher produced. The Critic receives its task plus the Analyst's conclusions plus the Researcher's background. By the time the Reporter runs it has the entire chain of reasoning available to draw from.

This is what makes the system coherent. Each agent builds on what came before rather than operating in isolation. The Optimizer knows not just what the Critic said — it also knows what the Analyst was trying to say and what the Researcher found. That context makes for much better improvements.

---

## Self-Reflection Loop

The Critic and Optimizer together form a self-reflection loop. The system reviews its own output, identifies weaknesses, and improves them before the user sees anything. This is one of the things that separates a sophisticated multi-agent system from a simple pipeline.

The Orchestrator includes this loop only when it adds genuine value — complex analytical tasks, strategy work, anything where quality matters more than speed. For a simple factual question the loop is skipped entirely.

The Validator after the loop ensures the improvements actually addressed the right things. It is possible for an Optimizer to "improve" an output in ways that move it away from what the user asked. The Validator catches this by always checking against the original query.

---

## Memory Integration

Nexus AI integrates the full three-layer memory system from Day 4. Before every query all three stores are searched and relevant context is injected into the Orchestrator's input. After every query the response is stored back.

This means the system gets smarter over time within a user's history. The first time you ask about a topic it starts from scratch. The second time it has context from the first conversation. Over time it builds a picture of what you work on, what you know, what you have asked before, and what was useful.

The memory files use separate names from Day 4 so they can coexist without conflict.

---

## Two Model Clients

The Orchestrator uses a smaller, faster model. Its job is to read a query and output a JSON plan — this requires clear thinking about task decomposition but does not require deep reasoning or rich knowledge. A fast model does this well and quickly.

The worker agents use a larger, more capable model. They need to produce high-quality research, write correct code, give honest critical feedback, and generate professional reports. The quality difference between a small and large model matters here in a way it does not for planning.

Separating the clients keeps the system fast where speed matters and powerful where quality matters.

---

## Failure Recovery

Every agent step retries once on failure before recording an error and moving on. Transient API errors, temporary rate limits, and occasional malformed model responses are handled gracefully without crashing the entire pipeline.

If a step fails after both attempts, the error message is stored in that step's output slot and the pipeline continues. The final answer may be missing one piece but the system does not stop. A partial answer is almost always better than a crash.

---

## Logging and Tracing

Every run creates a timestamped log file. The log captures every agent that ran, every completion, every failure, and the total time taken. This gives you a complete audit trail of exactly what happened during any run.

When something goes wrong you can open the log and trace the exact sequence of events — which agent failed, what error it produced, whether it retried, what the final output was. This kind of observability is what makes a system debuggable in production.

---

## The Streamlit Dashboard

Beyond the terminal interface, Nexus AI has a web dashboard built with Streamlit. It shows the execution tree with live status indicators — pending, active, and complete states for each step. Agent badges are color-coded by type so you can see at a glance which specialists are involved. The sidebar shows memory context retrieved for each query so you can see what the system remembered about you.

---

## Execution Flow Diagram

```
User types a query
    |
    v
[Memory Retrieval]
  Searches short-term, SQLite, and FAISS stores
  Injects relevant context into the query
    |
    v
[Orchestrator]
  Reads query + memory context
  Decides which agents are needed and in what order
  Produces JSON execution plan
    |
    v
[Sequential Execution — agents run in order]
  |
  ├── [PLANNER]     if task needs upfront planning
  |       |
  ├── [RESEARCHER]  background knowledge and facts
  |       |
  ├── [CODER]       if code needs to be written or executed
  |       |
  ├── [ANALYST]     patterns, insights, conclusions
  |       |
  ├── [CRITIC]      finds weaknesses in the analysis
  |       |
  ├── [OPTIMIZER]   improves based on critic feedback
  |       |
  ├── [VALIDATOR]   checks against original query
  |       |
  └── [REPORTER]    formats final report (only if requested)
    |
    v
[Memory Storage]
  Stores this exchange in all three memory layers
  Saves FAISS index and SQLite to disk
    |
    v
[Final Answer — printed to terminal or shown in dashboard]
```

---

## File Structure

```
Day5/
├── nexus_ai/
│   ├── agents/
│   │   ├── orchestrator.py    ← dynamic plan generator
│   │   ├── planner.py         ← detailed step breakdown
│   │   ├── researcher.py      ← background knowledge
│   │   ├── coder.py           ← Python execution
│   │   ├── analyst.py         ← patterns and insights
│   │   ├── critic.py          ← quality reviewer
│   │   ├── optimizer.py       ← output improver
│   │   ├── validator.py       ← correctness checker
│   │   ├── reporter.py        ← final report formatter
│   │   └── agents.py          ← registry mapping names to factories
│   ├── config.py              ← model clients and agent roster
│   └── main.py                ← pipeline with memory and logging
├── memory/
│   ├── session_memory.py      ← reused from Day 4
│   └── vector_store.py        ← reused from Day 4
├── logs/                      ← timestamped log file per run
├── app.py                     ← Streamlit dashboard
├── ARCHITECTURE.md            ← this file
└── README.md                  ← setup and usage
```

---

## How to Run

```bash
# terminal interface
cd Day5
python nexus_ai/main.py

# web dashboard
cd Day5
streamlit run app.py --server.fileWatcherType none
```

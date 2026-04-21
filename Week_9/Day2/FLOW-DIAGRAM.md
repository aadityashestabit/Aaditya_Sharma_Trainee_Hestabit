## From Fixed Chains to Dynamic Orchestration

Day 1 had three agents always running in the same order. Research, then Summarize, then Answer — every single time, regardless of what the user asked. That works for simple Q&A but falls apart the moment you need something more complex. Planning a startup is not the same kind of task as explaining a concept. One needs market research, competitor analysis, financial modeling, and product design. The other just needs a clear explanation. Treating them identically is wasteful and produces worse results.

Day 2 introduces orchestration. Instead of hardcoding which agents run and when, we have a Planner that reads the query and decides. Simple questions get a small plan. Complex tasks get a larger one. Tasks that can be done independently run at the same time. Tasks that need earlier results wait for them. The query determines the plan — not the code.

---

## What a DAG Is ??

DAG stands for Directed Acyclic Graph. The name sounds technical but the idea is simple enough that you use it every day without thinking about it.

When you cook a meal, some things can happen at the same time — you can boil water while you chop vegetables. Other things must happen in order — you cannot add pasta before the water boils, and you cannot serve the dish before the pasta is cooked. The relationships between tasks form a graph. The arrows between tasks point in one direction (directed) and nothing loops back on itself (acyclic).

That is a DAG. In our system each task is a node. An arrow from task A to task B means B depends on A and cannot start until A is done. Tasks with no incoming arrows can start immediately and run in parallel with each other. The executor figures out the optimal schedule automatically based on these relationships.

This is the same model used by Apache Airflow for data pipelines, Prefect for workflow automation, and LangGraph for agent systems. It is the industry standard for any system where work has dependencies.

---

## Structured Output with Pydantic

Getting the Planner to produce a reliable, parseable plan is harder than it sounds. If you just ask the model to output a numbered list, the formatting varies between runs. Sometimes it adds extra text. Sometimes the numbering is wrong. You end up writing fragile regex to parse it and the whole thing breaks when the model changes its mind about formatting.

Pydantic solves this by defining an exact schema that the model must conform to. Every Task must have a worker name, a description, and a list of dependencies. The entire Plan is a list of Tasks. When the Planner produces output, it gets validated against this schema immediately. If the model returns something that does not match — wrong field names, missing fields, malformed JSON — validation fails with a clear error rather than silently passing garbage to the next step.

This makes the system robust. You know exactly what shape the plan will be in before execution starts.

---

## How Workers Execute

Once the plan is ready, the DAG executor takes over. It looks at all the tasks in the plan and finds the ones that have no unmet dependencies. Those are the tasks that are ready to run right now. It runs all of them simultaneously using asyncio.gather — they all start at the same moment and the executor waits for all of them to finish before checking what is ready next.

As each task completes its output gets stored and marked as done. The executor then checks the remaining tasks again. Any task whose dependencies are now all completed becomes ready and starts running. This cycle continues until every task in the plan has been executed.

The result is that independent work happens in parallel and dependent work waits naturally. No explicit scheduling logic is needed — the dependency graph handles all of it.

---

## Controlling Parallelism with a Semaphore

Running too many tasks simultaneously causes problems. On Groq's free tier there is a limit on how many tokens per minute you can send. If ten tasks all start at the same moment and each sends a large prompt, you hit the rate limit and tasks start failing.

A semaphore is the standard solution. Think of it as a room with a fixed number of seats. Workers can only run if there is a seat available. When a worker finishes it frees its seat and the next queued worker can enter. With MAX_PARALLEL_WORKERS set to three, at most three tasks run simultaneously regardless of how many are ready. The others wait in a queue and start as slots open up.

This is the same mechanism used in every production task queue system — Celery, Ray, ThreadPoolExecutor. The number is tunable. On a paid API tier you can increase it. On a slow local machine you might decrease it.

---

## Reflection and Validation

After all worker tasks complete, two quality control steps always run. These are not part of the DAG — they are fixed steps that happen after everything else finishes.

The Reflection Agent receives the final worker output and reviews it. It looks for repetition, gaps, and weak sections and produces an improved version. It only receives the last task's output, not all outputs combined. The last worker already has context from all previous tasks injected into its prompt, so its output is already a synthesis of everything that came before.

The Validator receives the reflected output alongside the original user query. Its job is to check whether the final answer actually addresses what was asked. It either passes the output through unchanged or fixes whatever is missing. Giving the Validator the original query is important — without it the Validator does not know what standard to hold the output to.

---

## Execution Flow Diagram

```
User: "Plan a startup in AI for healthcare"
    |
    v
[Planner]
  Reads the query and generates a structured Plan (Pydantic validated)
    |
    v
[DAG Executor]
  ├── market_analysis_worker      depends on: none  ──┐
  ├── competitor_research_worker  depends on: none  ──┤ run in parallel
  └── regulation_research_worker  depends on: none  ──┘
                |
                v  (all three complete)
                |
  └── gap_analysis_worker  depends on: [market, competitor, regulation]
                |
                v
  └── business_plan_worker  depends on: [gap_analysis]
                |
                v
[All workers complete]
    |
    v
[Reflection Agent]
  Receives business_plan_worker output only
  Reviews, removes repetition, fills gaps
    |
    v
[Validator Agent]
  Receives: original query + reflected output
  Checks: does this actually answer "plan a startup in AI for healthcare"?
  Returns: improved version or passes through unchanged
    |
    v
[Final Answer printed to terminal]
```

---

## File Structure

```
Day2/
├── orchestrator/
│   └── planner.py          ← Pydantic schema (Task, Plan) + Planner agent
├── agents/
│   ├── worker_agent.py     ← generic worker spawned per task
│   ├── reflection_agent.py ← reviews and improves final output
│   └── validator_agent.py  ← checks output against original query
├── loader.py               ← LLM client with structured output enabled
├── run_day2.py             ← DAG executor with semaphore + retry
└── FLOW-DIAGRAM.md         ← this file
```
# FLOW-DIAGRAM.md
## Week 9 — Day 2: Multi-Agent Orchestration

---

## Architecture

```
User Query
    |
    v
[Orchestrator / Planner]
  - reads the query
  - breaks it into 3 subtasks
  - outputs a numbered task list
    |
    |-----> [Worker 1] -- subtask 1
    |-----> [Worker 2] -- subtask 2  (all 3 run in parallel via asyncio.gather)
    |-----> [Worker 3] -- subtask 3
    |
    v
[Reflection Agent]
  - receives all 3 worker outputs combined
  - removes repetition, fills gaps
  - improves overall quality and coherence
    |
    v
[Validator Agent]
  - checks for factual errors, contradictions, missing points
  - fixes issues if found
  - approves and outputs final answer
    |
    v
Final Answer
```

---

## Key Concepts

### Parallel Execution
Workers run simultaneously using `asyncio.gather()`:
```python
results = await asyncio.gather(
    run_worker(1, task1),
    run_worker(2, task2),
    run_worker(3, task3),
)
```
This is faster than running them one by one.

### Dynamic Task Planning
The Orchestrator reads the query and decides the subtasks at runtime.
No hardcoded task list — every query gets a different breakdown.

### Execution Tree
Printed at runtime to show what each worker is doing:
```
---- EXECUTION TREE ----
  Worker 1 -> Research the healthcare AI market
  Worker 2 -> Identify key competitors
  Worker 3 -> Suggest a business model
------------------------
```

### Reflection + Validation
Two quality-control stages after workers finish:
- Reflection: improves and merges the outputs
- Validator: final error check before the user sees anything

---

## File Structure

```
Day2/
├── orchestrator/
│   └── planner.py          <- breaks query into 3 subtasks
├── agents/
│   ├── worker_agent.py     <- reusable worker, spawned per task
│   ├── reflection_agent.py <- merges and improves worker outputs
│   └── validator_agent.py  <- final quality check
├── loader.py               <- LLM client config
├── run_day2.py             <- main pipeline runner
└── FLOW-DIAGRAM.md         <- this file
```

---

## How to Run

```bash
cd Day2
python run_day2.py
```
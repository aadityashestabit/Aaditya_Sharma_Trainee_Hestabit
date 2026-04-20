import asyncio
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen_agentchat.messages import TextMessage
from pydantic import ValidationError
from loader import LLMclient
from orchestrator.planner import Planner, Plan
from agents.worker_agent import get_worker
from agents.reflection_agent import get_reflection_agent
from agents.validator_agent import get_validator


MAX_PARALLEL_WORKERS = 3


def strip_markdown(text: str) -> str:
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def print_execution_tree(query: str, plan: Plan):
    print(f"\nUser: {query}")
    print("\n[DAG] Execution Tree")
    print(f"├── Query received")
    print(f"├── Planner generated {len(plan.tasks)} tasks")
    print(f"├── Max parallel workers: {MAX_PARALLEL_WORKERS}")
    print(f"├── [Task Structure]")
    for i, task in enumerate(plan.tasks):
        prefix = "└──" if i == len(plan.tasks) - 1 else "├──"
        deps   = ", ".join(task.depends_on) if task.depends_on else "none (parallel)"
        print(f"│   {prefix} [{task.worker_name}] {task.description[:55]}...")
        print(f"│       depends on: {deps}")

    parallel = [t.worker_name for t in plan.tasks if not t.depends_on]
    if len(parallel) > 1:
        print(f"├── Initial parallel batch: {parallel}")
    print(f"└── [Execution Started]")


async def run_task(task_name: str, task_text: str, dep_outputs: dict, client) -> str:
    worker    = get_worker(task_name, client)
    full_task = task_text

    if dep_outputs:
        context   = "\n\n".join([f"[{name}]\n{out[:400]}" for name, out in dep_outputs.items()])
        full_task = f"{task_text}\n\n--- Previous outputs ---\n{context}"

    for attempt in range(3):
        try:
            resp = await worker.on_messages(
                [TextMessage(content=full_task, source="user")],
                cancellation_token=None,
            )
            return strip_markdown(resp.chat_message.content)
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "429" in err or "too large" in err.lower():
                wait = 30 * (attempt + 1)
                print(f"│   [Rate limit] Waiting {wait}s... ({attempt+1}/3)")
                await asyncio.sleep(wait)
            else:
                return f"[{task_name} error: {err}]"

    return f"[{task_name} failed after 3 attempts]"


async def execute_plan(plan: Plan, client) -> dict:
    completed = {}
    remaining = {t.worker_name: t for t in plan.tasks}
    semaphore = asyncio.Semaphore(MAX_PARALLEL_WORKERS)

    while remaining:
        # find tasks whose dependencies are all done
        ready = [
            task for task in remaining.values()
            if all(dep in completed for dep in task.depends_on)
        ]

        if not ready:
            print("[Error] Deadlock — check depends_on values in plan")
            break

        batch = [t.worker_name for t in ready]
        if len(ready) > 1:
            active = min(len(ready), MAX_PARALLEL_WORKERS)
            print(f"\n├── [Parallel] {batch} ({active} active)")
        else:
            print(f"\n├── [Worker] Running [{ready[0].worker_name}]")

        async def run_one(task):
            async with semaphore:
                dep_outputs = {dep: completed[dep] for dep in task.depends_on}
                print(f"│   ├── WORKER → [{task.worker_name}]: {task.description[:55]}...")
                result = await run_task(task.worker_name, task.description, dep_outputs, client)
                await asyncio.sleep(1)
                return task.worker_name, result

        results = await asyncio.gather(*[run_one(t) for t in ready])

        for name, output in results:
            completed[name] = output
            del remaining[name]
            print(f"│   └── [{name}] complete ({len(output)} chars)")

    return completed


async def run_pipeline(user_query: str):
    client  = LLMclient().llmclient
    planner = Planner(client, worker_limit=MAX_PARALLEL_WORKERS * 2)

    # step 1 — planner creates structured plan
    print("\n[Planner] Building execution plan...")
    try:
        plan = await planner.run(user_query)
    except ValidationError as e:
        print(f"[Planner] Schema validation failed: {e}")
        return
    except Exception as e:
        print(f"[Planner Error] {e}")
        return

    print_execution_tree(user_query, plan)

    # step 2 — execute all tasks following dependency order
    completed = await execute_plan(plan, client)

    # step 3 — reflection on final task output only
    last_task   = plan.tasks[-1]
    last_output = completed.get(last_task.worker_name, "[No output]")

    print(f"\n├── [Reflection] Reviewing final output...")
    reflection = get_reflection_agent(client)
    try:
        ref_resp    = await reflection.on_messages(
            [TextMessage(content=last_output, source="user")],
            cancellation_token=None,
        )
        ref_output  = strip_markdown(ref_resp.chat_message.content)
    except Exception as e:
        ref_output  = last_output
        print(f"│   [Reflection error: {e}]")

    # step 4 — validator checks against original query
    print(f"├── [Validator] Checking against original query...")
    validator = get_validator(client)
    try:
        val_input   = f"Original query: {user_query}\n\nOutput to validate:\n{ref_output}"
        val_resp    = await validator.on_messages(
            [TextMessage(content=val_input, source="user")],
            cancellation_token=None,
        )
        final       = strip_markdown(val_resp.chat_message.content)
    except Exception as e:
        final       = ref_output
        print(f"│   [Validator error: {e}]")

    print(f"└── [Complete]")
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(final)
    print("=" * 60)

    return final


if __name__ == "__main__":
    query = input("Enter your query: ")
    asyncio.run(run_pipeline(query))
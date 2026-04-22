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


# removes markdown format 
def strip_markdown(text):
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# calls any agent and retries if rate limit is hit
async def call_agent(agent, message):
    for attempt in range(3):
        try:
            resp = await agent.on_messages(
                [TextMessage(content=message, source="user")],
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
                return f"[Error: {err}]"
    return "[Failed after 3 attempts]"


async def run_pipeline(user_query):
    client  = LLMclient().llmclient
    planner = Planner(client, worker_limit=MAX_PARALLEL_WORKERS * 2)

    # step 1 — planner builds the execution plan
    print("\n[Planner] Building execution plan...")
    try:
        plan = await planner.run(user_query)
    except ValidationError as e:
        print(f"[Planner] Schema validation failed:\n{e}")
        return
    except Exception as e:
        print(f"[Planner Error] {e}")
        return

    # print the execution tree
    print(f"\nUser: {user_query}")
    print("\n[DAG] Execution Tree")
    print(f"├── Planner generated {len(plan.tasks)} tasks")
    for i, task in enumerate(plan.tasks):
        prefix = "└──" if i == len(plan.tasks) - 1 else "├──"
        deps   = ", ".join(task.depends_on) if task.depends_on else "none (parallel)"
        print(f"│   {prefix} [{task.worker_name}] {task.description[:55]}...")
        print(f"│       depends on: {deps}")
    print(f"└── [Execution Started]")

    # step 2 — execute the DAG
    completed = {}                                          # stores finished task outputs
    remaining = {t.worker_name: t for t in plan.tasks}     # stores tasks not yet done
    semaphore = asyncio.Semaphore(MAX_PARALLEL_WORKERS)     # limits how many run at once

    while remaining:

        # find tasks where all dependencies are already completed
        ready = [
            task for task in remaining.values()
            if all(dep in completed for dep in task.depends_on)
        ]

        if not ready:
            print("[Error] Deadlock — circular dependency in plan")
            break

        # show what is about to run
        if len(ready) > 1:
            print(f"\n├── [Parallel] {[t.worker_name for t in ready]}")
        else:
            print(f"\n├── [Worker] Running [{ready[0].worker_name}]")

        # run all ready tasks at the same time, semaphore limits to MAX_PARALLEL_WORKERS
        async def run_one(task):
            async with semaphore:

                # build context from dependency outputs
                context = "\n\n".join(
                    [f"[{dep}]\n{completed[dep][:400]}" for dep in task.depends_on]
                )
                message = task.description
                if context:
                    message = f"{task.description}\n\n--- Previous outputs ---\n{context}"

                print(f"│   ├── WORKER → [{task.worker_name}]: {task.description[:55]}...")
                result = await call_agent(get_worker(task.worker_name, client), message)
                await asyncio.sleep(1)      # small pause to avoid burst rate limits
                return task.worker_name, result

        # launch all ready tasks simultaneously and wait for all to finish
        results = await asyncio.gather(*[run_one(t) for t in ready])

        for name, output in results:
            completed[name] = output
            del remaining[name]
            print(f"│   └── [{name}] complete ({len(output)} chars)")

    # step 3 — reflection reviews the final task output only
    print(f"\n├── [Reflection] Reviewing final output...")
    last_output = completed.get(plan.tasks[-1].worker_name, "[No output]")
    ref_output  = await call_agent(get_reflection_agent(client), last_output)

    # step 4 — validator checks output against the original query
    print(f"├── [Validator] Checking against original query...")
    val_input = f"Original query: {user_query}\n\nOutput to validate:\n{ref_output}"
    val_text  = await call_agent(get_validator(client), val_input)

    # if validator says PASS — show reflection output, not the verdict
    pass_phrases = ["pass", "the output fully", "unchanged", "correct and complete"]
    final = ref_output if any(p in val_text.lower() for p in pass_phrases) else val_text

    print(f"└── [Complete]")
    print("\n" + "-" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(final)
    print("=" * 60)

    return final


if __name__ == "__main__":
    asyncio.run(run_pipeline(input("Enter your query: ")))
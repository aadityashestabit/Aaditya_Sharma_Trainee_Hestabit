import asyncio
import json
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.model_context import BufferedChatCompletionContext
from loader import LLMclient, ToolLLMclient
from tools.file_agent import get_file_agent
from tools.db_agent import get_db_agent
from tools.code_executor import get_code_agent


PLANNER_PROMPT = """\
You are a task planner for a multi-agent tool pipeline. Given a user request, break it into an ordered list of steps.

AVAILABLE AGENTS:
  FILE  -> read files, write files, list directories (.txt, .csv, .md)
  DB    -> run SQL queries, create tables, insert small amounts of data (<50 rows)
  CODE  -> generate large datasets (50+ rows) programmatically and insert via Python
  CODE  -> write AND execute Python code in one step. Never split writing and running into separate steps

RULES:
  - Each step must be handled by exactly one agent: FILE, DB, or CODE.
  - Each step's task must be self-contained and reference outputs from previous steps where needed.
  - Only add a FILE save step if the user explicitly says "save", "store", "export", or "write to file".
  - For DB insert steps, always say "CREATE TABLE IF NOT EXISTS ... then INSERT".
  - Output ONLY a valid JSON array. No explanation, no markdown fences.

OUTPUT FORMAT:
[
  {"step": 1, "agent": "FILE", "task": "Read the file sales.csv and return its full content."},
  {"step": 2, "agent": "CODE", "task": "Using the CSV data provided, find the top 5 products by revenue."},
  {"step": 3, "agent": "FILE", "task": "Write the analysis results to report.txt"}
]
"""


def parse_plan(raw: str) -> list:
    # strip markdown fences if model wrapped in ```json
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

    try:
        plan = json.loads(raw)
        if isinstance(plan, list):
            return plan
    except json.JSONDecodeError:
        pass

    # fallback — try to find a JSON array anywhere in the output
    match = re.search(r'\[.*\]', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    # last resort — treat the whole thing as a single code task
    print("[Planner] Could not parse JSON plan. Running as single CODE step.")
    return [{"step": 1, "agent": "CODE", "task": raw}]


async def run_pipeline():
    planner_client = LLMclient().llmclient  
    tool_client    = ToolLLMclient().llmclient

    # planner decides which agents to call and in what order
    planner = AssistantAgent(
        name="planner",
        system_message=PLANNER_PROMPT,
        model_client=planner_client,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )

    # tool agents — each has real tools registered
    agents = {
        "FILE": get_file_agent(tool_client),
        "DB":   get_db_agent(tool_client),
        "CODE": get_code_agent(tool_client),
    }

    print("\n=== Day 3: Tool-Calling Agent Pipeline ===")
    print("  Agents  : FILE | DB | CODE")
    print("  Mode    : Sequential chaining")
    print("  Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("User: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Shutting down]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("[Shutting down]")
            break

        # step 1 - planner figures out what needs to happen
        print("\n[Planner] Thinking...")
        planner_resp = await planner.on_messages(
            [TextMessage(content=user_input, source="user")],
            cancellation_token=None,
        )
        raw_plan = planner_resp.chat_message.content
        plan = parse_plan(raw_plan)

        # show the plan
        print(f"\n[Plan] {len(plan)} step(s) identified:")
        for step in plan:
            print(f"  Step {step['step']} -> [{step['agent']}] {step['task'][:80]}...")

        # step 2 - run each agent in order, passing previous outputs forward
        all_outputs = []

        for step in plan:
            agent_key = step["agent"].upper()
            task = step["task"]

            # inject all previous outputs so each agent has full context
            if all_outputs:
                previous = "\n\n".join(all_outputs)
                full_task = f"{task}\n\n--- Outputs from previous steps ---\n{previous}"
            else:
                full_task = task

            print(f"\n[Step {step['step']}] {agent_key} Agent working...")

            if agent_key not in agents:
                print(f"  [Warning] Unknown agent '{agent_key}' — skipping.")
                continue

            try:
                resp = await agents[agent_key].on_messages(
                    [TextMessage(content=full_task, source="user")],
                    cancellation_token=None,
                )
                result = resp.chat_message.content
                all_outputs.append(f"[Step {step['step']} - {agent_key}]\n{result}")
                print(f"\n[{agent_key} Result]\n{result}")

            except Exception as e:
                error_msg = f"[Error in {agent_key}] {str(e)}"
                all_outputs.append(f"[Step {step['step']} - {agent_key}]\n{error_msg}")
                print(f"  {error_msg}")

        print("\n" + "─" * 50)
        print("[Pipeline complete]")
        print("─" * 50)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
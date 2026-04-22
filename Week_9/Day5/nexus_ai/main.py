import asyncio
import json
import os
import re
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.messages import TextMessage
from nexus_ai.config import get_model_client, get_planner_client, MAX_PLAN_STEPS, AGENT_ROSTER, get_tool_client
from nexus_ai.agents.orchestrator import get_orchestrator
from nexus_ai.agents.agents import get_agent
from memory.session_memory import SessionMemory
from memory.vector_store import FaissVectorStore


#  logging

os.makedirs("logs", exist_ok=True)
os.makedirs("memory", exist_ok=True)

log_file = f"logs/nexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
    ]
)

# suppress extra logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("autogen_core").setLevel(logging.WARNING)

logger = logging.getLogger("nexus")


# plan parsing 

def parse_plan(raw: str) -> list:
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

    try:
        plan = json.loads(raw)
        if isinstance(plan, list):
            return plan[:MAX_PLAN_STEPS]
    except json.JSONDecodeError:
        pass

    match = re.search(r'\[.*\]', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())[:MAX_PLAN_STEPS]
        except Exception:
            pass

    logger.warning("Could not parse orchestrator plan — defaulting to RESEARCHER")
    return [{"step": 1, "agent": "RESEARCHER", "task": raw}]


# execution tree display 

def print_execution_tree(query: str, plan: list):
    print(f"\nUser: {query}")
    print("\n[NEXUS AI] Execution Tree")
    print(f"├── Query received")
    print(f"├── Orchestrator generated {len(plan)} step plan")
    print(f"├── [Execution Started]")
    for i, step in enumerate(plan, 1):
        prefix = "└──" if i == len(plan) else "├──"
        agent = step.get("agent", "UNKNOWN")
        task  = step.get("task", "")[:70]
        print(f"│   {prefix} Step {step['step']} [{agent}]: {task}...")


# memory context builder

def build_memory_context(recent: str, facts: str, vectors: str) -> str:
    # only include sections that actually have content
    sections = []
    if recent != "No recent conversation yet.":
        sections.append(f"Recent conversation:\n{recent}")
    if facts != "No relevant facts found.":
        sections.append(f"Relevant facts from memory:\n{facts}")
    if vectors != "No similar context found.":
        sections.append(f"Related past context:\n{vectors}")

    if not sections:
        return ""
    return "--- Memory Context ---\n" + "\n\n".join(sections) + "\n--- End Memory ---"


# main pipeline 
async def run_nexus(user_query: str, session: SessionMemory, vector_store: FaissVectorStore):
    logger.info(f"New query: {user_query}")

    # 1 — retrieve from all 3 memory stores before doing anything
    fact_hits    = session.search_facts(user_query, limit=5)
    vector_hits  = vector_store.search(user_query, k=3)
    recent       = session.format_recent_context()
    fact_context = session.format_fact_results(fact_hits)
    vec_context  = vector_store.format_search_results(vector_hits)

    memory_context = build_memory_context(recent, fact_context, vec_context)

    # inject memory into the query so orchestrator and all agents have context
    if memory_context:
        enriched_query = f"{memory_context}\n\nCurrent query: {user_query}"
        print(f"\n[Memory] Retrieved context from {len(fact_hits)} facts + {len(vector_hits)} vectors")
    else:
        enriched_query = user_query

    TOOL_AGENTS = {"CODER", "FILE", "DB"}
    planner_client = get_planner_client()
    worker_client  = get_model_client()
    tool_client = get_tool_client()

    # 2 — orchestrator creates the dynamic plan
    orchestrator = get_orchestrator(planner_client)

    logger.info("Orchestrator planning...")
    try:
        plan_resp = await orchestrator.on_messages(
            [TextMessage(content=enriched_query, source="user")],
            cancellation_token=None,
        )
        raw_plan = plan_resp.chat_message.content
        plan = parse_plan(raw_plan)
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
        return None

    print_execution_tree(user_query, plan)

    # 3 — run each agent in order, passing all previous outputs forward
    all_outputs = []

    for step in plan:
        agent_name = step.get("agent", "").upper()
        task       = step.get("task", "")

        if agent_name not in AGENT_ROSTER:
            logger.warning(f"Step {step['step']}: unknown agent '{agent_name}' — skipping")
            continue

        # inject previous outputs + memory so each agent has full context
        if all_outputs:
            history   = "\n\n".join(all_outputs)
            full_task = f"{task}\n\n--- Previous step outputs ---\n{history}"
        else:
            full_task = task

        # inject memory into first step only — keeps prompt size manageable
        if memory_context and not all_outputs:
            full_task = f"{memory_context}\n\n{full_task}"

        logger.info(f"Step {step['step']} — {agent_name} starting")
        print(f"\n├── [Step {step['step']}] {agent_name} working...")

        client = tool_client if agent_name in TOOL_AGENTS else worker_client
        agent  = get_agent(agent_name, client)
        if not agent:
            logger.warning(f"Could not create agent '{agent_name}' — skipping")
            continue

        # failure recovery — retry once on error
        result = None
        for attempt in range(2):
            try:
                resp = await agent.on_messages(
                    [TextMessage(content=full_task, source="user")],
                    cancellation_token=None,
                )
                result = resp.chat_message.content
                break
            except Exception as e:
                logger.warning(f"Step {step['step']} attempt {attempt+1} failed: {e}")
                if attempt == 1:
                    result = f"[{agent_name} failed after 2 attempts: {str(e)}]"

        all_outputs.append(f"[Step {step['step']} — {agent_name}]\n{result}")
        logger.info(f"Step {step['step']} — {agent_name} complete ({len(result)} chars)")

    print(f"\n└── [Execution Complete]")

    final = all_outputs[-1] if all_outputs else "[No output generated]"
    clean_final = re.sub(r'^\[Step \d+ — \w+\]\n', '', final)

    print("\n" + "=" * 60)
    print("NEXUS AI — FINAL REPORT")
    print("=" * 60)
    print(clean_final)
    print("=" * 60)

    # step 4 — store this interaction back into all memory stores
    session.add_turn("user", user_query)
    session.add_turn("assistant", clean_final)

    user_facts      = session.extract_important_facts(user_query)
    assistant_facts = session.extract_important_facts(clean_final)
    session.store_facts(user_facts + assistant_facts)

    vector_store.add_text(user_query,   {"role": "user"})
    vector_store.add_text(clean_final,  {"role": "assistant"})

    logger.info(f"Memory updated. Log saved to {log_file}")
    return clean_final


async def main():
    # initialise memory once — shared across all queries in this session
    session = SessionMemory(
        db_path="memory/nexus_long_term.db",
        max_turns=10,
    )
    vector_store = FaissVectorStore(
        index_path="memory/nexus_vector.index",
        metadata_path="memory/nexus_vector_metadata.pkl",
    )

    print("-----------------NEXUS AI-----------------")
    print(f"\nAgents   : {', '.join(AGENT_ROSTER.keys())}")
    print(f"Memory   : SQLite + FAISS ({vector_store.total_vectors} vectors loaded)")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            query = input("User: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Shutting down Nexus AI]")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            print("[Shutting down Nexus AI]")
            break

        await run_nexus(query, session, vector_store)
        print()


if __name__ == "__main__":
    asyncio.run(main())
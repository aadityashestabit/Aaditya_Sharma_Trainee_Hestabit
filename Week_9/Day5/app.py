import streamlit as st
import asyncio
import json
import os
import re
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen_agentchat.messages import TextMessage
from nexus_ai.config import get_model_client, get_planner_client, MAX_PLAN_STEPS, AGENT_ROSTER
from nexus_ai.agents.orchestrator import get_orchestrator
from nexus_ai.agents.agents import get_agent
from memory.session_memory import SessionMemory
from memory.vector_store import FaissVectorStore

# suppress noisy logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("autogen_core").setLevel(logging.WARNING)

# ── page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Nexus AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── custom styling ────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e2e2e8;
}

/* sidebar */
section[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e2e;
}

/* header */
.nexus-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 24px 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 24px;
}
.nexus-logo {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6af7, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.nexus-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #4a4a6a;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* agent badge */
.agent-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1px;
    margin: 2px;
}

/* chat messages */
.user-msg {
    background: #13131f;
    border: 1px solid #2a2a3e;
    border-radius: 12px 12px 4px 12px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 15px;
    color: #c4c4d4;
}
.assistant-msg {
    background: #0f0f1c;
    border: 1px solid #7c6af7;
    border-left: 3px solid #7c6af7;
    border-radius: 4px 12px 12px 12px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 14px;
    color: #d4d4e8;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
    line-height: 1.6;
}

/* execution step */
.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    margin: 4px 0;
    background: #0d0d1a;
    border-radius: 8px;
    border-left: 2px solid #2a2a3e;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #6a6a8a;
}
.step-item.active {
    border-left-color: #7c6af7;
    color: #a8a8d0;
    background: #13132a;
}
.step-item.done {
    border-left-color: #22c55e;
    color: #86efac;
}

/* memory panel */
.memory-card {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 14px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #5a5a7a;
    line-height: 1.6;
}
.memory-label {
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #4a4a6a;
    margin-bottom: 6px;
}

/* input */
.stTextInput input {
    background: #0f0f1a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #e2e2e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
}

/* buttons */
.stButton button {
    background: linear-gradient(135deg, #7c6af7, #60a5fa) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 8px 20px !important;
}
.stButton button:hover {
    opacity: 0.9 !important;
}

/* metric cards */
.metric-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #a78bfa;
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #4a4a6a;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

hr { border-color: #1e1e2e; }
</style>
""", unsafe_allow_html=True)


# ── agent colors ──────────────────────────────────────────────────────────────

AGENT_COLORS = {
    "PLANNER":    "#f59e0b",
    "RESEARCHER": "#3b82f6",
    "CODER":      "#10b981",
    "ANALYST":    "#8b5cf6",
    "CRITIC":     "#ef4444",
    "OPTIMIZER":  "#f97316",
    "VALIDATOR":  "#06b6d4",
    "REPORTER":   "#ec4899",
}


def agent_badge(name: str) -> str:
    color = AGENT_COLORS.get(name.upper(), "#6b7280")
    return f'<span class="agent-badge" style="background:{color}22;color:{color};border:1px solid {color}44">{name}</span>'


# ── memory & state init ───────────────────────────────────────────────────────

@st.cache_resource
def init_memory():
    os.makedirs("memory", exist_ok=True)
    session = SessionMemory(db_path="memory/nexus_long_term.db", max_turns=10)
    vector_store = FaissVectorStore(
        index_path="memory/nexus_vector.index",
        metadata_path="memory/nexus_vector_metadata.pkl",
    )
    return session, vector_store


session_mem, vector_store = init_memory()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "execution_steps" not in st.session_state:
    st.session_state.execution_steps = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "last_memory_context" not in st.session_state:
    st.session_state.last_memory_context = ""


# ── pipeline helpers ──────────────────────────────────────────────────────────

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
    return [{"step": 1, "agent": "RESEARCHER", "task": raw}]


def build_memory_context(recent, facts, vectors) -> str:
    sections = []
    if recent != "No recent conversation yet.":
        sections.append(f"Recent conversation:\n{recent}")
    if facts != "No relevant facts found.":
        sections.append(f"Relevant facts:\n{facts}")
    if vectors != "No similar context found.":
        sections.append(f"Related past context:\n{vectors}")
    if not sections:
        return ""
    return "--- Memory Context ---\n" + "\n\n".join(sections) + "\n--- End Memory ---"


async def run_pipeline(user_query: str, step_placeholder, status_placeholder):
    # memory retrieval
    fact_hits    = session_mem.search_facts(user_query, limit=5)
    vector_hits  = vector_store.search(user_query, k=3)
    recent       = session_mem.format_recent_context()
    fact_context = session_mem.format_fact_results(fact_hits)
    vec_context  = vector_store.format_search_results(vector_hits)
    memory_ctx   = build_memory_context(recent, fact_context, vec_context)

    st.session_state.last_memory_context = memory_ctx if memory_ctx else "No memory retrieved for this query."

    enriched_query = f"{memory_ctx}\n\nCurrent query: {user_query}" if memory_ctx else user_query

    planner_client = get_planner_client()
    worker_client  = get_model_client()

    # orchestrator planning
    status_placeholder.markdown("**Orchestrator** planning execution...")
    orchestrator = get_orchestrator(planner_client)
    try:
        plan_resp = await orchestrator.on_messages(
            [TextMessage(content=enriched_query, source="user")],
            cancellation_token=None,
        )
        plan = parse_plan(plan_resp.chat_message.content)
    except Exception as e:
        return f"[Orchestrator Error] {e}"

    # show planned steps
    steps_html = "".join([
        f'<div class="step-item">⬡ Step {s["step"]} {agent_badge(s["agent"])} — {s["task"][:60]}...</div>'
        for s in plan
    ])
    step_placeholder.markdown(steps_html, unsafe_allow_html=True)

    # run agents
    all_outputs = []
    for step in plan:
        agent_name = step.get("agent", "").upper()
        task       = step.get("task", "")

        if agent_name not in AGENT_ROSTER:
            continue

        # update step display — mark current as active
        steps_html = "".join([
            f'<div class="step-item {"active" if s["step"] == step["step"] else "done" if s["step"] < step["step"] else ""}">'
            f'{"▶" if s["step"] == step["step"] else "✓" if s["step"] < step["step"] else "⬡"} '
            f'Step {s["step"]} {agent_badge(s["agent"])} — {s["task"][:55]}...</div>'
            for s in plan
        ])
        step_placeholder.markdown(steps_html, unsafe_allow_html=True)
        status_placeholder.markdown(f"**{agent_name}** working...")

        if all_outputs:
            history   = "\n\n".join(all_outputs)
            full_task = f"{task}\n\n--- Previous step outputs ---\n{history}"
        else:
            full_task = f"{memory_ctx}\n\n{task}" if memory_ctx else task

        agent  = get_agent(agent_name, worker_client)
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
                if attempt == 1:
                    result = f"[{agent_name} failed: {e}]"

        all_outputs.append(f"[Step {step['step']} — {agent_name}]\n{result}")

    # mark all done
    steps_html = "".join([
        f'<div class="step-item done">✓ Step {s["step"]} {agent_badge(s["agent"])} — {s["task"][:55]}...</div>'
        for s in plan
    ])
    step_placeholder.markdown(steps_html, unsafe_allow_html=True)
    status_placeholder.markdown("**Complete** ✓")

    final = all_outputs[-1] if all_outputs else "[No output]"
    clean = re.sub(r'^\[Step \d+ — \w+\]\n', '', final)

    # store to memory
    session_mem.add_turn("user", user_query)
    session_mem.add_turn("assistant", clean)
    session_mem.store_facts(session_mem.extract_important_facts(user_query))
    session_mem.store_facts(session_mem.extract_important_facts(clean))
    vector_store.add_text(user_query, {"role": "user"})
    vector_store.add_text(clean,      {"role": "assistant"})

    return clean, plan


# ── layout ────────────────────────────────────────────────────────────────────

# sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0">
        <div style="font-family: Syne; font-size: 22px; font-weight: 800;
                    background: linear-gradient(135deg, #7c6af7, #60a5fa);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent">
            ⬡ NEXUS AI
        </div>
        <div style="font-family: JetBrains Mono; font-size: 9px; color: #3a3a5a;
                    letter-spacing: 2px; text-transform: uppercase; margin-top: 2px">
            Multi-Agent System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.total_queries}</div>
            <div class="metric-label">Queries</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{vector_store.total_vectors}</div>
            <div class="metric-label">Vectors</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="memory-label">Agents</div>', unsafe_allow_html=True)
    badges = " ".join([agent_badge(a) for a in AGENT_ROSTER.keys()])
    st.markdown(badges, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="memory-label">Memory Context</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="memory-card">{st.session_state.last_memory_context or "No memory retrieved yet."}</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.execution_steps = []
        st.session_state.total_queries = 0
        st.rerun()

# main area
st.markdown("""
<div class="nexus-header">
    <div>
        <div class="nexus-logo">⬡ NEXUS AI</div>
        <div class="nexus-sub">Autonomous Multi-Agent System — Day 5</div>
    </div>
</div>
""", unsafe_allow_html=True)

# chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# input row
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input(
        label="query",
        placeholder="Ask Nexus AI anything...",
        label_visibility="collapsed",
        key="user_input"
    )
with col_btn:
    send = st.button("Send →", use_container_width=True)

# execution panel
if send and user_input.strip():
    query = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.total_queries += 1

    with st.expander("⬡ Execution Tree", expanded=True):
        step_placeholder   = st.empty()
        status_placeholder = st.empty()

        try:
            result = asyncio.run(run_pipeline(query, step_placeholder, status_placeholder))
            if isinstance(result, tuple):
                answer, plan = result
            else:
                answer = result
        except Exception as e:
            answer = f"[Pipeline Error] {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
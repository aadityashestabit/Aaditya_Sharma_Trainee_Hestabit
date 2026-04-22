import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

AGENT_ROSTER = {
    "PLANNER":    "Creates a detailed step-by-step plan for the task",
    "RESEARCHER": "Gathers background knowledge, facts, and context",
    "CODER":      "Writes and executes Python code",
    "ANALYST":    "Analyzes data, finds patterns, draws conclusions",
    "CRITIC":     "Reviews output and identifies weaknesses or gaps",
    "OPTIMIZER":  "Improves output based on Critic feedback",
    "VALIDATOR":  "Checks final output for correctness and completeness",
    "REPORTER":   "Formats everything into a polished final report",
    "FILE":       "Reads and writes files (.txt, .csv, .md, any text format)",
    "DB":         "Creates and queries SQLite databases with SQL",
}

MAX_PLAN_STEPS = 10

# switch between "ollama" and "groq"
ACTIVE_PROVIDER = "ollama"


def get_model_client():
    # standard client — no tool calling, used by most agents
    if ACTIVE_PROVIDER == "ollama":
        return OpenAIChatCompletionClient(
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
            api_key="not-required",
            model_info={
                "family": "openai",
                "context_length": 8192,
                "function_calling": False,
                "vision": False,
                "json_output": False,
                "structured_output": False,
            }
        )
    else:
        return OpenAIChatCompletionClient(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["LLM_API_KEY"],
            model_info={
                "family": "openai",
                "context_length": 131072,
                "function_calling": False,
                "vision": False,
                "json_output": False,
                "structured_output": False,
            }
        )


def get_tool_client():
    # tool client — function calling enabled, used by CODER, FILE, DB agents
    if ACTIVE_PROVIDER == "ollama":
        return OpenAIChatCompletionClient(
            model="qwen2.5:7b",
            base_url="http://localhost:11434/v1",
            api_key="not-required",
            model_info={
                "family": "openai",
                "context_length": 8192,
                "function_calling": True,
                "vision": False,
                "json_output": False,
                "structured_output": False,
            }
        )
    else:
        return OpenAIChatCompletionClient(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["LLM_API_KEY"],
            model_info={
                "family": "openai",
                "context_length": 131072,
                "function_calling": True,
                "vision": False,
                "json_output": False,
                "structured_output": False,
            }
        )


def get_planner_client():
    # planner uses the same provider but always with function_calling off
    return get_model_client()
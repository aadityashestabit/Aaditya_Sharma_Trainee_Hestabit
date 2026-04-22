from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool
from tools.code_executor import run_python


def get_coder(model_client):
    return AssistantAgent(
        name="coder",
        description="Writes and executes Python code to solve technical tasks.",
        system_message=(
            "You are the Coder of NEXUS AI. You write and execute Python code.\n\n"
            "YOUR TOOL: run_python(code) — runs Python in a subprocess.\n"
            "Missing packages are auto-installed before running.\n\n"
            "RULES:\n"
            "- Always call run_python() — never skip execution.\n"
            "- Write COMPLETE runnable code with all imports included.\n"
            "- Use print() for every result — that is the only thing captured.\n"
            "- If execution fails, read the error, fix the code, and retry.\n"
            "- Never use placeholders or '...' in the code.\n\n"
            "CSV OUTPUT RULE:\n"
            "If the output will be saved as CSV in a later step, always print\n"
            "the full dataset as a JSON array of dicts:\n"
            "  import json\n"
            "  rows = [{'col1': val1, 'col2': val2}, ...]\n"
            "  print(json.dumps(rows))\n\n"
            "RESPONSE RULES:\n"
            "- User asked to show/write/display code -> include [CODE] and [OUTPUT]\n"
            "- User asked to run/calculate/analyse  -> include only [OUTPUT]\n"
            "- When in doubt, include both.\n"
            "Plain text only. No markdown."
        ),
        model_client=model_client,
        tools=[
            FunctionTool(run_python, description="Execute Python code and return the code and its output"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
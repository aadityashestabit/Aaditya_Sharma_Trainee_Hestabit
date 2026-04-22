import re
import subprocess
import sys
import tempfile
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool


# maps import names to their actual pip package names where they differ
IMPORT_TO_PIP = {
    "sklearn":  "scikit-learn",
    "cv2":      "opencv-python",
    "PIL":      "Pillow",
    "bs4":      "beautifulsoup4",
    "yaml":     "pyyaml",
    "dotenv":   "python-dotenv",
    "dateutil": "python-dateutil",
}


def _extract_imports(code: str) -> list:
    # pull out the top-level package name from every import/from line
    pattern = re.compile(
        r'^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.MULTILINE
    )
    seen = []
    for match in pattern.finditer(code):
        pkg = match.group(1)
        if pkg not in seen:
            seen.append(pkg)
    return seen


def _auto_install(code: str) -> None:
    # try importing each package — install it if missing
    for name in _extract_imports(code):
        try:
            __import__(name)
            continue
        except ImportError:
            pass

        pip_name = IMPORT_TO_PIP.get(name, name)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_name, "-q"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[auto-install] Installed: {pip_name}")
        else:
            print(f"[auto-install] Could not install {pip_name}: {result.stderr[:80]}")


def run_python(code: str) -> str:
    # auto-install any missing packages before running
    _auto_install(code)
    
    import textwrap
    code = textwrap.dedent(code).strip()
    
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0:
            output = f"{stdout}\n[Errors]\n{stderr}" if stdout else f"[Errors]\n{stderr}"
        else:
            output = stdout if stdout else "Script ran successfully with no output."

        # return both code and output so next agent in chain can see both
        return f"[CODE]\n{code}\n\n[OUTPUT]\n{output}"

    except subprocess.TimeoutExpired:
        return "[Error] Code timed out after 30 seconds."
    except Exception as e:
        return f"[Error] Could not execute code: {e}"
    finally:
        try:
            if tmp_path:
                os.unlink(tmp_path)
        except Exception:
            pass


def get_code_agent(model_client):
    return AssistantAgent(
        name="code_agent",
        system_message=(
            "You are a Code Agent. You write and execute Python code to solve tasks.\n"
            "You MUST call run_python() to execute the code.\n"
            "Do NOT write code as text. Do NOT explain the code.\n"
            "ONLY call the run_python tool with the complete code.\n"
            "YOUR TOOL: run_python(code) — runs Python in a subprocess. Auto-installs missing packages.\n\n"
            "RULES:\n"
            "- Always call run_python() — never skip execution.\n"
            "- Write COMPLETE runnable code with all imports included.\n"
            "- Use print() for every result — that is the only thing captured in output.\n"
            "- You can use any library: pandas, numpy, csv, statistics etc. Missing ones are installed automatically.\n"
            "- If execution fails, read the error, fix the code, and retry.\n"
            "- Never use placeholders or '...' in the code.\n\n"
            "CSV OUTPUT RULE:\n"
            "If the task produces data that a later step will save as CSV, always print the full dataset as a JSON array:\n"
            "  import json\n"
            "  rows = [{'col1': val1, 'col2': val2}, ...]\n"
            "  print(json.dumps(rows))\n"
            "Never truncate with head() when the data will be saved.\n\n"
            "RESPONSE RULES:\n"
            "- User asked to show/write/display code → include [CODE] and [OUTPUT] in reply.\n"
            "- User asked to run/calculate/analyse → include only [OUTPUT] in reply.\n"
            "- A later step needs to save the code to a file → always include [CODE] so FILE agent can write it.\n"
            "- When in doubt, include both.\n"
            "Plain text only. No markdown."
        ),
        model_client=model_client,
        tools=[
            FunctionTool(run_python, description="Execute Python code and return the code and its output"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
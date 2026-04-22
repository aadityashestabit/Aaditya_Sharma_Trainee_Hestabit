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

BLOCKED_PATTERNS = [
    r'os\.remove\s*\(',
    r'os\.unlink\s*\(',
    r'shutil\.rmtree\s*\(',
    r'shutil\.move\s*\(',
    r'os\.rmdir\s*\(',
    r'subprocess.*rm\s',
    r'subprocess.*del\s',
]

def _is_dangerous(code: str) -> bool:
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return True
    return False


def _extract_imports(code: str) -> list:
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
    
    if _is_dangerous(code):
        return "[Error] Code contains a blocked operation (delete/remove). Execution refused."
    _auto_install(code)
    
    import textwrap
    code = textwrap.dedent(code).strip() #indent
    
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
        system_message=("""
        You are a Code Agent. Your ONLY job is to call run_python() immediately.
        Do NOT write markdown. Do NOT write ## steps. Do NOT use code blocks.
        Do NOT explain anything. Do NOT narrate. Just call the tool.

        YOUR TOOL: run_python(code) — executes Python in a real subprocess.
        Missing packages are auto-installed before running.

        RULES:
        1. Always call run_python() — never skip execution.
        2. Write COMPLETE runnable code — all imports must be at the top.
        3. Always write code on MULTIPLE LINES with proper indentation.
           Never put multiple statements on one line using semicolons.
           Functions, loops, and if statements must always be on separate indented lines.
        4. Use print() for every result — that is the only thing captured in output.
        5. Never use placeholders like '...' or 'pass' in the code.
        6. If execution fails — read the error, fix the code, call run_python() again.
        7. For charts always use plt.savefig('filename.png') — never plt.show().
           plt.show() hangs in terminal. Always call plt.close() after saving.

        IF THE TASK SAYS save code / write code to a file / create a script:
           Do NOT execute the code.
           Print the code as a plain string so FILE agent can save it.
           Example: print(code_string)

        IF A LATER STEP WILL SAVE THE OUTPUT AS CSV:
           Always print the full dataset as a JSON array — never truncate.
           Example:
             import json
             rows = [{'col1': val1, 'col2': val2}, ...]
             print(json.dumps(rows))

        RESPONSE FORMAT:
        - Task says show/write/display code    - include [CODE] and [OUTPUT]
        - Task says run/calculate/analyse      - include only [OUTPUT]
        - A later step needs to save the code  - always include [CODE]
        - When in doubt                        - include both

        Plain text only. No markdown. No asterisks. No headers. Just call the tool.
        """),
        model_client=model_client,
        tools=[
            FunctionTool(run_python, description="Execute Python code and return the code and its output"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
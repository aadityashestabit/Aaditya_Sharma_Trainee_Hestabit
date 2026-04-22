import csv
import os
import json
import statistics
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool


def read_file(file_path: str) -> str:
    try:
        if file_path.lower().endswith(".csv"):
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                columns = list(reader.fieldnames or [])

            if not rows:
                return f"[Info] '{file_path}' is empty."

            lines = [
                f"CSV file: {file_path}",
                f"  {len(rows)} rows x {len(columns)} columns",
                f"  Columns: {', '.join(columns)}",
                "",
                "---Rows ---",
            ]
            for i, row in enumerate(rows, 1):
                lines.append(f"  {i:>3}. " + " | ".join(f"{k}={v}" for k, v in row.items()))

            # per-column stats so the CODE agent knows what it's working with
            lines.append("")
            lines.append("── Column Statistics ──")
            for col in columns:
                values = [r[col] for r in rows if r.get(col, "").strip() != ""]
                try:
                    nums = [float(v) for v in values]
                    mean = statistics.mean(nums)
                    stdev = statistics.stdev(nums) if len(nums) > 1 else 0.0
                    lines.append(
                        f"  [{col}] numeric  count={len(nums)}  "
                        f"min={min(nums):.2f}  max={max(nums):.2f}  "
                        f"mean={mean:.2f}  stdev={stdev:.2f}"
                    )
                except ValueError:
                    unique = list(dict.fromkeys(values))
                    lines.append(
                        f"  [{col}] text  count={len(values)}  "
                        f"unique={len(unique)}  sample={unique[:5]}"
                    )
            return "\n".join(lines)

        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    except FileNotFoundError:
        return f"[Error] File not found: {file_path}"
    except Exception as e:
        return f"[Error] read_file failed: {e}"


def write_file(file_path: str, content: str) -> str:
    try:
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"[OK] Wrote {len(content)} chars to '{file_path}'"
    except Exception as e:
        return f"[Error] write_file failed: {e}"


def write_csv(file_path: str, rows: list) -> str:
    # accepts list of dicts, list of lists, or a JSON string
    try:
        if not rows:
            return "[Error] write_csv: no rows provided."

        if isinstance(rows, str):
            try:
                rows = json.loads(rows)
            except json.JSONDecodeError:
                return "[Error] write_csv: could not parse JSON string."

        # normalise to list of dicts
        if isinstance(rows[0], dict):
            dict_rows = rows
        elif isinstance(rows[0], (list, tuple)):
            if all(isinstance(v, str) for v in rows[0]):
                headers = list(rows[0])
                dict_rows = [dict(zip(headers, r)) for r in rows[1:]]
            else:
                headers = [f"col_{i}" for i in range(len(rows[0]))]
                dict_rows = [dict(zip(headers, r)) for r in rows]
        else:
            return f"[Error] write_csv: unrecognised row type: {type(rows[0])}"

        if not dict_rows:
            return "[Error] write_csv: no data rows after normalisation."

        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=dict_rows[0].keys())
            writer.writeheader()
            writer.writerows(dict_rows)

        return f"[OK] '{file_path}' written — {len(dict_rows)} rows, {len(dict_rows[0])} columns"

    except Exception as e:
        return f"[Error] write_csv failed: {e}"


def append_file(file_path: str, content: str) -> str:
    try:
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"[OK] Appended {len(content)} chars to '{file_path}'"
    except Exception as e:
        return f"[Error] append_file failed: {e}"


def list_files(directory: str = ".") -> str:
    try:
        entries = os.listdir(directory)
        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
        if not files:
            return f"[Info] No files found in '{directory}'"
        return "\n".join(files)
    except Exception as e:
        return f"[Error] list_files failed: {e}"


def get_file_agent(model_client):
    return AssistantAgent(
        name="file_agent",
        system_message=("""
        You are a File Agent. You ONLY act by calling your tools.
        Never write Python code to do file operations.
        Never narrate or explain what you are about to do.
        Call a tool immediately — that is your only valid response.

        WHEN WRITING A CSV FROM PREVIOUS STEP OUTPUT:
        1. Parse the JSON array from the previous output using json.loads()
        2. Call write_csv(file_path, rows) with the parsed list
        3. Do NOT re-embed all rows inside the tool call — just pass the variable
        The previous step output is already available as context — use it directly.

        YOUR TOOLS:
          read_file(file_path)            - reads any file. CSVs also return column statistics.
          write_file(file_path, content)  - writes text to any file (.txt, .md, .py etc.)
          write_csv(file_path, rows)      - writes a properly formatted CSV from list of dicts
          append_file(file_path, content) - adds content to an existing file
          list_files(directory)           - lists all files in a folder

        DECISION RULES:
          Task says READ?             - call read_file()
          Task says WRITE a .csv?     - call write_csv()  never write_file for CSVs
          Task says WRITE a .txt/.md? - call write_file()
          Task says APPEND?           - call append_file()
        Task says LIST?             - call list_files()
        
        BLOCKED OPERATIONS:
        - Never delete, remove, or destroy any file under any circumstance.
        - If the user asks to delete a file, respond: Delete operations are not permitted.
        - There is no delete tool and you must not attempt to work around this.


        RULES:
        1. Always call a tool immediately. Never fake or guess file contents.
        2. For CSV creation use write_csv() with rows as a list of dicts.
        3. For text/report creation use write_file() with the full content from the previous step.
        4. After the tool succeeds, report only the tool result.
        5. Never use write_file for .csv files — it won't escape commas correctly.

        Plain text only. No markdown.
        """),
        model_client=model_client,
        tools=[
            FunctionTool(read_file,    description="Read any file. CSVs also return column statistics."),
            FunctionTool(write_file,   description="Write text content to a file"),
            FunctionTool(write_csv,    description="Write a CSV file from a list of dicts or JSON string"),
            FunctionTool(append_file,  description="Append content to an existing file"),
            FunctionTool(list_files,   description="List files in a directory"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
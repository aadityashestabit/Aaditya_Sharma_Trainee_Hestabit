import sqlite3
import os
import re
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool


def inspect_schema(db_path: str) -> str:
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row # - return dict object
            cur = conn.cursor()

            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'") # filter only tables 
            tables = [row["name"] for row in cur.fetchall()]

            if not tables:
                return f"[Info] '{db_path}' exists but has no tables yet. Proceed to CREATE."

            lines = [f"Schema for: {db_path}", "=" * 40]

            for table in tables:
                cur.execute(f'PRAGMA table_info("{table}")') # return metadata 
                columns = cur.fetchall()
                cur.execute(f'SELECT COUNT(*) as total FROM "{table}"')
                total = cur.fetchone()["total"]

                lines.append(f"\nTable: {table}  ({total} rows)")
                lines.append("Columns:")
                for col in columns:
                    pk_label = " PRIMARY KEY" if col["pk"] else ""
                    lines.append(f"  {col['name']}  {col['type']}{pk_label}")

                # showing sample rows
                cur.execute(f'SELECT * FROM "{table}" LIMIT 3')
                samples = [dict(r) for r in cur.fetchall()]
                if samples:
                    lines.append("Sample rows (first 3):")
                    for row in samples:
                        lines.append("  " + ", ".join(f"{k}={v}" for k, v in row.items()))

            lines.append("\n" + "=" * 40)
            return "\n".join(lines)

    except Exception as e:  
        return f"[Error] inspect_schema failed: {e}"


def execute_sql(db_path: str, query: str) -> str:
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # multi-statement scripts 
            is_script = ";" in query and not query.strip().upper().startswith(("SELECT", "WITH", "PRAGMA"))
            if is_script:
                cur.executescript(query)
                conn.commit() #save

                inserted_tables = re.findall(r"INSERT\s+INTO\s+(\w+)", query, re.IGNORECASE)
                if inserted_tables:
                    counts = []
                    for t in set(inserted_tables):
                        try:
                            cur.execute(f'SELECT COUNT(*) FROM "{t}"')
                            n = cur.fetchone()[0]
                            counts.append(f"{t}: {n} rows")
                        except Exception:
                            pass
                    if counts:
                        return f"[OK] Script executed. Row counts: {', '.join(counts)}"
                return "[OK] Script executed successfully."

            # single statement
            cur.execute(query)

            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
                conn.commit()
                return f"[OK] Executed. Rows affected: {cur.rowcount}"

            # SELECT 
            rows = [dict(r) for r in cur.fetchall()]
            if not rows:
                return "[Info] Query returned no rows."

            header = " | ".join(rows[0].keys())
            divider = "─" * len(header)
            body = "\n".join(" | ".join(str(v) for v in row.values()) for row in rows)
            return f"{header}\n{divider}\n{body}"

    except Exception as e:
        return f"[Error] execute_sql failed: {e}"


def get_db_agent(model_client):
    return AssistantAgent(
        name="db_agent",
        system_message=(
            """
            You are a Database Agent. You work with SQLite databases.
            You MUST call execute_sql() or inspect_schema() immediately.
            Do NOT write SQL as text. Do NOT explain. Just call the tool.
            If no database path is specified, use 'data.db' as the default.

            YOUR TOOLS:
              inspect_schema(db_path)     - shows all tables, columns, row counts, and sample rows
              execute_sql(db_path, query) - runs SQL and returns the result

            RULES:
            1. Always call inspect_schema() first to see what already exists.
               If it says 'has no tables' — that is normal. Proceed to CREATE.
               Never stop just because the database is empty.
            2. When inserting data, always do CREATE TABLE IF NOT EXISTS then INSERT in one script.
               Combine both into a single execute_sql() call.
            3. After inserting, always verify the row count with SELECT COUNT(*).
               If count is 0, the insert failed — fix and retry.
            4. For append tasks, never use fixed ID values.
               Omit the primary key column so SQLite auto-increments correctly.
            5. Always pass db_path explicitly in every tool call.
            6. SQLite does not support CREATE DATABASE — create a table instead.
            7. If a query fails, read the error, fix the SQL, and retry.
            Plain text only. No markdown.
            """
        ),
        model_client=model_client,
        tools=[
            FunctionTool(inspect_schema, description="Show all tables, columns, and sample rows in a SQLite database"),
            FunctionTool(execute_sql,    description="Run a SQL query or script on a SQLite database"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
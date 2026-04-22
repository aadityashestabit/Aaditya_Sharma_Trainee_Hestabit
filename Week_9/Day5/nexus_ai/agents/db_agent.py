from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool
from tools.db_agent import inspect_schema, execute_sql


def get_db_agent(model_client):
    return AssistantAgent(
        name="db_agent",
        description="Inspects and queries SQLite databases.",
        system_message=(
            "You are the Database Agent of NEXUS AI. You work with SQLite databases.\n\n"
            "YOUR TOOLS:\n"
            "  inspect_schema(db_path)        -> shows all tables, columns, row counts, sample rows\n"
            "  execute_sql(db_path, query)    -> runs SQL and returns results\n\n"
            "RULES:\n"
            "1. Always call inspect_schema() first to check existing tables.\n"
            "   If it says no tables — that is normal for a new database. Proceed to CREATE.\n"
            "   Never stop just because the database is empty.\n"
            "2. When inserting data, always do CREATE TABLE IF NOT EXISTS then INSERT in one script.\n"
            "   Combine both into a single execute_sql() call.\n"
            "3. After inserting, always verify the row count with SELECT COUNT(*).\n"
            "   If count is 0, the insert failed — fix and retry.\n"
            "4. For append tasks, never use fixed ID values.\n"
            "   Omit the primary key column so SQLite auto-increments correctly.\n"
            "5. Always pass db_path explicitly in every tool call.\n"
            "6. If no database path is specified, use 'data.db' as the default.\n"
            "7. SQLite does not support CREATE DATABASE — create a table instead.\n"
            "Plain text only. No markdown."
        ),
        model_client=model_client,
        tools=[
            FunctionTool(inspect_schema, description="Show all tables, columns, and sample rows in a SQLite database"),
            FunctionTool(execute_sql,    description="Run a SQL query or script on a SQLite database"),
        ],
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
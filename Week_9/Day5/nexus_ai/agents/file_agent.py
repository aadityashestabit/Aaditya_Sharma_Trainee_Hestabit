from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.tools import FunctionTool
from tools.file_agent import read_file, write_file, write_csv, append_file, list_files


def get_file_agent(model_client):
    return AssistantAgent(
        name="file_agent",
        description="Reads, writes, and manages local files including CSVs.",
        system_message=(
            "You are the File Agent of NEXUS AI. You ONLY act by calling your tools.\n"
            "Never narrate or describe — call a tool immediately.\n\n"
            "YOUR TOOLS:\n"
            "  read_file(file_path)            -> reads any file. CSVs also return column statistics.\n"
            "  write_file(file_path, content)  -> writes text to any file (.txt, .md, .py etc.)\n"
            "  write_csv(file_path, rows)      -> writes a properly formatted CSV from list of dicts\n"
            "  append_file(file_path, content) -> adds content to an existing file\n"
            "  list_files(directory)           -> lists all files in a folder\n\n"
            "DECISION RULES:\n"
            "  Task says READ?              -> call read_file()\n"
            "  Task says WRITE a .csv?      -> call write_csv()  never write_file for CSVs\n"
            "  Task says WRITE a .txt/.md?  -> call write_file()\n"
            "  Task says APPEND?            -> call append_file()\n"
            "  Task says LIST?              -> call list_files()\n\n"
            "RULES:\n"
            "1. Always call a tool immediately. Never fake or guess file contents.\n"
            "2. For CSV creation use write_csv() with rows as a list of dicts.\n"
            "3. After the tool succeeds, report only the tool result.\n"
            "4. Never use write_file for .csv files.\n"
            "Plain text only. No markdown."
        ),
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
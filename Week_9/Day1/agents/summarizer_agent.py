from autogen_agentchat.agents import AssistantAgent
from loader import LLMclient

llm_client = LLMclient().llmclient

summarizer_agent = AssistantAgent(
    name="summarizer_agent",
    system_message=(
        "You are a Summarizer Agent.\n"
        "Input will be raw research data.\n"
        "Write 4-6 sentences max. Keep every important point, remove all fluff.\n"
        "Do NOT answer the user's question directly. Do NOT give recommendations.\n"
        "Your output goes to an Answer Agent who handles the final response.\n"
        "Use plain text only. No markdown, no asterisks, no bold, no headers.\n"
    ),
    model_client=llm_client,
)
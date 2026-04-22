from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from loader import LLMclient


def get_research_agent():
    return AssistantAgent(
        name="research_agent",
        system_message=(
            "You are a Research Agent. Answer strictly from your training knowledge. "
            "Write factual bullet points in plain text only. "
            "Do NOT summarize or give a final answer. "
            "Use plain text only. No markdown, no asterisks, no bold, no headers."
        ),
        model_client=LLMclient().llmclient,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
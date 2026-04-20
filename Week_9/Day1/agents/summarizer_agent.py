from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.cache import ChatCompletionCache
from autogen_core.model_context import BufferedChatCompletionContext
from loader import LLMclient


def get_summarizer_agent():
    return AssistantAgent(
        name="summarizer_agent",
        system_message=(
            "You are a Summarizer Agent. Input will be raw research data. "
            "Write 4-6 sentences max. Keep every important point, remove all fluff. "
            "Do NOT answer the user's question directly. Do NOT give recommendations. "
            "Use plain text only. No markdown, no asterisks, no bold, no headers."
        ),
        model_client=LLMclient().llmclient,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
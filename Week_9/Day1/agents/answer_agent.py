from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.cache import ChatCompletionCache
from autogen_core.model_context import BufferedChatCompletionContext
from loader import LLMclient


def get_answer_agent():
    return AssistantAgent(
        name="answer_agent",
        system_message=(
            "You are an Answer Agent. "
            "Answer ONLY using the provided summary. Be concise and relevant to the question. "
            "Use plain text only. No markdown, no asterisks, no bold, no headers."
        ),
        model_client=LLMclient().llmclient,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
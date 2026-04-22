from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext


def get_reflection_agent(model_client):
    return AssistantAgent(
        name="reflection_agent",
        system_message=(
            """
            You are a Reflection Agent. You receive the final worker output.
            
            Review it, remove repetition, fill gaps, and improve coherence.
            
            Return the full improved version. Plain text only. No markdown.
            """
        ),
        model_client=model_client,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
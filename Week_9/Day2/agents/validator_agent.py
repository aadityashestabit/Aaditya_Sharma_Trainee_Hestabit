from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext


def get_validator(model_client):
    return AssistantAgent(
        name="validator",
        system_message=(
            "You are a Validator Agent. Check if the output fully answers the original query.\n"
            "If it is complete and accurate — return it unchanged.\n"
            "If something critical is missing — add it and return the improved version.\n"
            "Do not nitpick minor style issues. Plain text only. No markdown."
        ),
        model_client=model_client,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
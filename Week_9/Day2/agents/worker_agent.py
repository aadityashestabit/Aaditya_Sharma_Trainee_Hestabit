from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext


def get_worker(worker_name: str, model_client):
    return AssistantAgent(
        name=worker_name,
        system_message=(
            """
            You are a Worker Agent. Complete the assigned task thoroughly and factually. 
            
            If previous task outputs are provided, build on them. 
            
            Be detailed but concise. Plain text only. No markdown.
            """
         
        ),
        model_client=model_client,
        model_context=BufferedChatCompletionContext(buffer_size=10),
    )
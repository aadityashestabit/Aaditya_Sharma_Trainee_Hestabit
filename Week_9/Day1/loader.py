import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

class LLMclient:
    ## Creates and configures single LLM client that every agent can use
    def __init__(self):
        self.llmclient = OpenAIChatCompletionClient(
            model="openai/gpt-oss-120b",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ["LLM_API_KEY"],
            model_info={
                "family": "openai",
                "context_length": 8192,
                "function_calling": False,
                "vision": False,
                "json_output": False,
                "structured_output": False,
            }
        )
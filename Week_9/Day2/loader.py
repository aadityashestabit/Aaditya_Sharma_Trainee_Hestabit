import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class LLMclient:
    def __init__(self):
        self.llmclient = OpenAIChatCompletionClient(
            model="llama-3.1-8b-instant",
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
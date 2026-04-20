from typing import List
from pydantic import BaseModel, Field
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.model_context import BufferedChatCompletionContext


#  Pydantic schema

class Task(BaseModel):
    worker_name: str       = Field(..., description="Unique worker name e.g. worker_research")
    description: str       = Field(..., description="What this worker must do")
    depends_on: List[str]  = Field(default=[], description="worker_names this task depends on")


class Plan(BaseModel):
    tasks: List[Task] = Field(..., description="List of tasks for worker agents")


# Planner agent 

class Planner:
    def __init__(self, model_client, worker_limit: int = 5):
        self.worker_limit = worker_limit
        self.agent = AssistantAgent(
            name="planner",
            system_message=(
                "You are a Planner Agent. Break the user request into tasks for worker agents.\n\n"
                f"RULES:\n"
                f"- Maximum {worker_limit} worker tasks total.\n"
                "- Tasks with no depends_on run in parallel.\n"
                "- Tasks that need another task output must list it in depends_on.\n"
                "- Each task must be specific and self-contained.\n"
                "- worker_name must be unique, lowercase, with underscores.\n\n"
                "Return ONLY valid JSON matching this exact schema:\n"
                '{"tasks": [{"worker_name": "...", "description": "...", "depends_on": []}]}\n'
                "No explanation, no extra text, no markdown."
            ),
            model_client=model_client,
            model_context=BufferedChatCompletionContext(buffer_size=10),
        )

    async def run(self, user_task: str) -> Plan:
        response = await self.agent.run(
            task=TextMessage(content=user_task, source="user")
        )
        raw = response.messages[-1].content
        plan = Plan.model_validate_json(raw)
        return plan
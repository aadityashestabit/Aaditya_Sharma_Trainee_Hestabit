from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.model_context import BufferedChatCompletionContext


# schema — defines what one task looks like
class Task(BaseModel):
    worker_name: str
    description: str
    depends_on:  list = []      # no dependency by default 


# schema — the full plan is just a list of tasks
class Plan(BaseModel):
    tasks: list[Task]


# planner agent — reads the query and returns a validated Plan
class Planner:
    def __init__(self, model_client, worker_limit=5):
        self.agent = AssistantAgent(
            name="planner",
            system_message=(f"""
            You are a Planner Agent. Break the user request into tasks for worker agents.

            RULES:
            - Maximum {worker_limit} worker tasks total.
            - Tasks with no depends_on run in parallel.
            - Tasks that need another task output must list it in depends_on.
            - Each task must be specific and self-contained.
            - worker_name must be unique, lowercase, with underscores.

            Return ONLY valid JSON matching this exact schema:
            {{"tasks": [{{"worker_name": "...", "description": "...", "depends_on": []}}]}}

            No explanation, no extra text, no markdown.
            """),
            model_client=model_client,
            model_context=BufferedChatCompletionContext(buffer_size=10),
        )

    async def run(self, user_task):
        # sending query to groq and waiting for response 
        response = await self.agent.run(
            task=TextMessage(content=user_task, source="user")
        )
        raw  = response.messages[-1].content
        plan = Plan.model_validate_json(raw)  # JSON string - Python object and validates every field against schema 
        return plan
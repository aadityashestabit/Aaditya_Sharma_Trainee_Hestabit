from nexus_ai.agents.planner    import get_planner
from nexus_ai.agents.researcher import get_researcher
from nexus_ai.agents.coder      import get_coder
from nexus_ai.agents.analyst    import get_analyst
from nexus_ai.agents.critic     import get_critic
from nexus_ai.agents.optimizer  import get_optimizer
from nexus_ai.agents.validator  import get_validator
from nexus_ai.agents.reporter   import get_reporter


# maps agent name string to its factory function
AGENT_REGISTRY = {
    "PLANNER":    get_planner,
    "RESEARCHER": get_researcher,
    "CODER":      get_coder,
    "ANALYST":    get_analyst,
    "CRITIC":     get_critic,
    "OPTIMIZER":  get_optimizer,
    "VALIDATOR":  get_validator,
    "REPORTER":   get_reporter,
}


def get_agent(name: str, model_client):
    factory = AGENT_REGISTRY.get(name.upper())
    if not factory:
        return None
    return factory(model_client)
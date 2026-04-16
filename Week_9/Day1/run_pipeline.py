import asyncio
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent


async def run_pipeline(user_query: str):

    # stage 1 - research
    research_result = await research_agent.run(task=user_query)
    research_text = research_result.messages[-1].content
    print("\n-------------RESEARCH RESULT---------------")
    print(research_text)

    # stage 2 - summarize
    summary_result = await summarizer_agent.run(task=research_text)
    summary_text = summary_result.messages[-1].content
    print("\nSUMMARY RESULT :")
    print(summary_text)

    # stage 3 - final answer
    final_result = await answer_agent.run(task=summary_text)
    final_text = final_result.messages[-1].content
    print("\nFINAL RESULT :")
    print(final_text)

    return final_text


if __name__ == "__main__":
    query = input("What would you like to research ? ")
    asyncio.run(run_pipeline(query))
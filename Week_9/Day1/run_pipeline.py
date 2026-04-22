import asyncio
from agents.research_agent import get_research_agent
from agents.summarizer_agent import get_summarizer_agent
from agents.answer_agent import get_answer_agent


async def run_pipeline(user_query: str):
    # These are the pre configured agents 
    research_agent = get_research_agent()
    summarizer_agent = get_summarizer_agent()
    answer_agent = get_answer_agent()

    # stage 1 - research
    research_result = await research_agent.run(task=user_query)
    research_text = research_result.messages[-1].content
    print("\n-------------RESEARCH RESULT-----------------")
    print(research_text)

    # stage 2 - summarize
    summary_result = await summarizer_agent.run(task=research_text)
    summary_text = summary_result.messages[-1].content
    print("\n-------------SUMMARY RESULT ------------------")
    print(summary_text)

    # stage 3 - final answer
    # Passing both user query and summary to answer agent for result 
    final_result = await answer_agent.run(task=f"User question: {user_query}\n\nSummary: {summary_text}")
    final_text = final_result.messages[-1].content
    print("\n--------------FINAL RESULT---------------------")
    print(final_text)

    return final_text


if __name__ == "__main__":
    query = input("What would you like to research ? ")
    asyncio.run(run_pipeline(query))
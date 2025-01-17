import crewai
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import tool

# Import the LLM class
from crewai import LLM
    
llm=LLM(
    model="ollama/mannix/phi3-mini-4k"
)

def callback_function(output):
    print(f"Task completed: {output.raw_output}")

@tool("DuckDuckGoSearch")
def search(search_query: str) -> str:
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(search_query)

agent = crewai.Agent(
    role="Calendar",
    goal="What day of the month is Thanksgiving on in the current year?",
    backstory="You are a calendar assistant. You provide information about dates. ",
    tools=[search],
    llm=llm,
    allow_delegation=False, verbose=True)

task = crewai.Task(description="What day of the month is Thanksgiving on in the current year?",
                   agent=agent,
                   expected_output="Date of Thanksgiving in the current year")

crew = crewai.Crew(agents=[agent], tasks=[task], verbose=True)
res = crew.kickoff()
print(res)

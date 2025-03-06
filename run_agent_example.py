from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

# Create a custom LLM using OpenRouter
llm = LLM(
    model="openai/gpt-3.5-turbo",  # This will be routed through OpenRouter
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Create a simple agent
researcher = Agent(
    role="Research Analyst",
    goal="Conduct thorough analysis on given topics",
    backstory="You are an experienced research analyst with expertise in gathering and synthesizing information.",
    verbose=True,
    llm=llm  # Use the custom LLM
)

# Create a task for the agent
research_task = Task(
    description="Research and summarize the key features of crewAI",
    expected_output="A comprehensive summary of crewAI's key features",
    agent=researcher
)

# Create a crew with the agent and task
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# Run the crew
result = crew.kickoff()

# Print the result
print("\n\n========================")
print("FINAL RESULT:")
print(result.raw)
print("========================")
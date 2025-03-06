import os
from openai import OpenAI

# A simple function to simulate an agent with accurate information about crewAI
def run_accurate_agent():
    # Use OpenRouter API key
    client = OpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Define the agent's role and task with accurate information about crewAI
    system_message = """
    You are a Research Analyst agent with the following attributes:
    - Role: Research Analyst specializing in AI frameworks
    - Goal: Conduct thorough analysis on AI agent frameworks
    - Backstory: You are an experienced research analyst with expertise in AI systems and frameworks.
    
    Your task is to research and summarize the key features of crewAI, which is a framework for orchestrating role-playing autonomous AI agents.
    
    Here are some facts about crewAI to include in your analysis:
    1. crewAI is a framework for creating and orchestrating autonomous AI agents that can work together to accomplish complex tasks.
    2. It allows developers to create agents with specific roles, goals, and backstories.
    3. Agents can use tools to interact with external systems and APIs.
    4. crewAI supports different collaboration processes like sequential and hierarchical.
    5. It provides memory capabilities for agents to remember past interactions.
    6. The framework supports YAML configuration for easier agent and task definition.
    7. crewAI is built in Python and integrates with various LLM providers.
    """
    
    # Run the agent (simulate by making an API call)
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Research and summarize the key features of crewAI. Provide a comprehensive summary focusing on its capabilities as an AI agent framework."}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Print the result
    print("\n\n========================")
    print("ACCURATE AGENT RESULT:")
    print(response.choices[0].message.content)
    print("========================")

if __name__ == "__main__":
    run_accurate_agent()
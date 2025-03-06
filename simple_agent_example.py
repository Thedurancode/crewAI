import os
from openai import OpenAI

# A simple function to simulate an agent
def run_simple_agent():
    # Use OpenRouter API key
    client = OpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Define the agent's role and task
    system_message = """
    You are a Research Analyst agent with the following attributes:
    - Role: Research Analyst
    - Goal: Conduct thorough analysis on given topics
    - Backstory: You are an experienced research analyst with expertise in gathering and synthesizing information.
    
    Your task is to research and summarize the key features of crewAI.
    """
    
    # Run the agent (simulate by making an API call)
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Research and summarize the key features of crewAI. Provide a comprehensive summary."}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Print the result
    print("\n\n========================")
    print("AGENT RESULT:")
    print(response.choices[0].message.content)
    print("========================")

if __name__ == "__main__":
    run_simple_agent()
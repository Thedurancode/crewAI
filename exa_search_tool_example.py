from crewai import Agent
from crewai_tools import ExaSearchTool
import os

# Example of how to create and use the EXA search tool with the Research Agent

def create_research_agent_with_exa():
    """
    Creates a Research Agent with EXA search capabilities
    
    This example shows how to integrate the EXA API with the Research Agent
    to enable web searches for partnership research.
    """
    
    # Set your EXA API key (replace with your actual key)
    exa_api_key = os.environ.get("EXA_API_KEY", "your_exa_api_key_here")
    
    # Create the EXA search tool
    exa_search_tool = ExaSearchTool(
        api_key=exa_api_key,
        # Optional parameters for customizing search behavior
        highlight_results=True,
        num_results=10,
        use_autoprompt=True
    )
    
    # Create the Research Agent with the EXA tool
    research_agent = Agent(
        role="Research Agent",
        goal="Perform in-depth research on potential partners and advertisers for MLSE",
        backstory="You are an expert research agent with advanced capabilities in data gathering and analysis. You specialize in conducting comprehensive web searches, extracting relevant business information, and identifying potential partnership opportunities for MLSE.",
        verbose=True,
        tools=[exa_search_tool]  # Assign the EXA tool to the agent
    )
    
    return research_agent

def example_research_query(agent, query):
    """
    Example of how to use the Research Agent with a specific query
    
    Args:
        agent: The Research Agent with EXA tool
        query: The research query to execute
    
    Returns:
        The research results
    """
    # This simulates a task execution with a specific query
    # In the actual implementation, this would be handled by the crew task system
    result = agent.execute_task(
        f"Research the following potential partner for MLSE: {query}. "
        "Include information about their business model, previous sponsorships, "
        "financial health, and potential alignment with MLSE brands."
    )
    
    return result

if __name__ == "__main__":
    # Create the Research Agent with EXA tool
    research_agent = create_research_agent_with_exa()
    
    # Example usage
    company_to_research = "Nike"
    print(f"\nResearching potential partner: {company_to_research}\n")
    
    # Execute the research query
    research_results = example_research_query(research_agent, company_to_research)
    
    # Print the results
    print("\n========================")
    print("RESEARCH RESULTS:")
    print(research_results)
    print("========================")
    
    # Usage instructions
    print("\nTo use this with your own EXA API key:")
    print("1. Export your EXA API key as an environment variable:")
    print("   export EXA_API_KEY=your_actual_key_here")
    print("2. Run this script to test the EXA search functionality")
    print("3. Integrate this tool with the full MLSE Partnership Crew system")
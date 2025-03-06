# MLSE Partnership Research Crew

This system uses crewAI to create a team of specialized AI agents that work together to research, analyze, and present partnership opportunities for MLSE (Maple Leaf Sports & Entertainment).

## System Overview

The MLSE Partnership Research Crew consists of 9 specialized agents that collaborate to:

1. Gather information on current partners and potential advertisers
2. Conduct in-depth research using various data sources
3. Identify gaps in current partnerships
4. Evaluate potential partners using a scoring system
5. Refine research prompts for better results
6. Manage and organize research data
7. Monitor and optimize the research workflow
8. Create engaging video presentations
9. Generate professional PDF slideshows

## Agents

### Partner Knowledge Agent
- **Role**: Gathers and maintains information on current partners and potential advertisers
- **Capabilities**:
  - Identify and categorize current partners
  - Track potential advertisers
  - Retrieve and store relevant business details

### Research Agent
- **Role**: Performs in-depth research on potential partners and advertisers
- **Capabilities**:
  - Conduct web searches via EXA API and other sources
  - Extract and analyze relevant partner data
  - Identify potential business opportunities
  - Compile research reports

### Gap Identification Agent
- **Role**: Analyzes research data to identify gaps and opportunities
- **Capabilities**:
  - Compare partner data with industry trends
  - Highlight missing partnership categories
  - Recommend potential partners

### Partner Fit Score Agent
- **Role**: Evaluates potential partners using a scoring system
- **Capabilities**:
  - Assign a partner fit score based on predefined criteria
  - Analyze financial health and business alignment
  - Compare potential partners against current MLSE partners
  - Provide recommendations based on scoring insights

### Prompt Refinement Agent
- **Role**: Fine-tunes search queries and prompts
- **Capabilities**:
  - Optimize search prompts for accuracy
  - Refine queries based on retrieved data quality
  - Ensure relevant and high-quality research results

### Data Management Agent
- **Role**: Handles viewing, verifying, and saving research data
- **Capabilities**:
  - Verify data consistency
  - Prevent duplicate entries
  - Store structured data efficiently
  - Maintain historical research records

### Flow Review Agent
- **Role**: Oversees the entire research and data processing workflow
- **Capabilities**:
  - Monitor workflow execution
  - Identify and resolve process bottlenecks
  - Ensure smooth collaboration between agents

### Video Presentation Agent
- **Role**: Creates engaging video presentations
- **Capabilities**:
  - Generate video presentations from structured research data
  - Incorporate branding elements
  - Export and distribute video assets

### PDF Slideshow Agent
- **Role**: Generates professional PDF slideshows
- **Capabilities**:
  - Format research insights into slides
  - Ensure visual appeal and readability
  - Export PDFs for distribution

## Tasks

The system executes the following tasks in sequence:

1. **Gather Partner Data**: Identify and categorize current MLSE partners and potential advertisers
2. **Conduct Partner Research**: Perform in-depth research on potential partners using various sources
3. **Identify Partnership Gaps**: Analyze current portfolio to identify partnership opportunities
4. **Evaluate Partner Fit**: Score potential partners based on multiple criteria
5. **Refine Research Prompts**: Optimize search queries for better research results
6. **Manage Research Data**: Organize and store partnership research data
7. **Review Research Workflow**: Monitor and optimize the multi-agent research process
8. **Create Video Presentation**: Generate engaging video presentations of findings
9. **Generate PDF Slideshow**: Create professional PDF slideshows of research results

## Setup and Usage

### Prerequisites

Make sure you have crewAI installed:

```bash
pip install crewai
```

You'll also need to set up an API key for your preferred LLM provider. The default configuration uses OpenRouter, but you can modify it to use any provider supported by crewAI.

### Configuration

1. Edit the `config/agents.yaml` file to customize agent roles, goals, and backstories
2. Edit the `config/tasks.yaml` file to customize task descriptions and expected outputs
3. Update the `run_mlse_partnership_crew.py` file with your API key and preferred LLM model

### Running the Crew

To run the MLSE Partnership Research Crew:

```bash
python run_mlse_partnership_crew.py
```

This will execute all tasks in sequence and output the final result.

## Customization

### Adding New Agents

To add a new agent:

1. Add the agent configuration to `config/agents.yaml`
2. Create a new agent method in the `MLSEPartnershipCrew` class in `run_mlse_partnership_crew.py`
3. Add any new tasks for the agent in `config/tasks.yaml`
4. Create task methods in the `MLSEPartnershipCrew` class

### Changing the Process

The default process is sequential, but you can change it to hierarchical by modifying the `process` parameter in the `crew` method:

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.hierarchical,  # Changed from sequential
        verbose=True,
    )
```

### Adding Tools

You can enhance agent capabilities by adding tools. For example, to add the EXA search tool:

```python
from crewai_tools import ExaSearchTool

exa_search_tool = ExaSearchTool(api_key="your_exa_api_key")

@agent
def research_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['research_agent'],
        verbose=True,
        llm=llm,
        tools=[exa_search_tool]
    )
```

## Extending the System

This system can be extended in various ways:

1. **Add more data sources**: Integrate additional research tools and APIs
2. **Implement real-time updates**: Add agents that monitor news and market changes
3. **Create interactive dashboards**: Add agents that generate interactive visualizations
4. **Integrate with CRM systems**: Connect with existing customer relationship management tools
5. **Add feedback loops**: Implement mechanisms to improve results based on user feedback
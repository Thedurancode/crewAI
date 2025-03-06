# crewAI Agent Examples

This directory contains examples of how to create and run agents using crewAI.

## Prerequisites

Make sure you have crewAI installed:

```bash
pip install crewai
```

You may also need to set up an OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Basic Example

The `run_agent_example.py` file contains a basic example of creating and running a single agent:

```bash
python run_agent_example.py
```

This example:
1. Creates a simple research agent
2. Assigns it a task to research crewAI
3. Runs the agent and displays the result

## Advanced Example with Agent Builder

The `run_agent_with_builder.py` file demonstrates the agent builder pattern using YAML configuration:

```bash
python run_agent_with_builder.py
```

This example:
1. Uses YAML configuration files in the `config` directory
2. Creates multiple agents (researcher and writer)
3. Sets up tasks with dependencies between them
4. Uses the `CrewBase` decorator to simplify agent and task creation

### Configuration Files

- `config/agents.yaml`: Contains the configuration for the agents
- `config/tasks.yaml`: Contains the configuration for the tasks

## Understanding the Code

### Agent Creation

Agents are created with a role, goal, and backstory:

```python
agent = Agent(
    role="Research Analyst",
    goal="Conduct thorough analysis on given topics",
    backstory="You are an experienced research analyst...",
    verbose=True
)
```

### Task Creation

Tasks are created with a description, expected output, and assigned agent:

```python
task = Task(
    description="Research and summarize the key features of crewAI",
    expected_output="A comprehensive summary of crewAI's key features",
    agent=agent
)
```

### Crew Creation

A crew is created with a list of agents and tasks:

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)
```

### Running the Crew

The crew is run with the `kickoff()` method:

```python
result = crew.kickoff()
```

## Agent Builder Pattern

The agent builder pattern uses decorators to simplify agent and task creation:

```python
@CrewBase
class MyCrew():
    @agent
    def my_agent(self) -> Agent:
        return Agent(config=self.agents_config['my_agent'])
    
    @task
    def my_task(self) -> Task:
        return Task(config=self.tasks_config['my_task'])
    
    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)
```

This pattern makes it easier to manage complex crews with multiple agents and tasks.
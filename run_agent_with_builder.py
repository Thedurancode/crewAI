from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ContentCreationCrew():
    """Crew for creating content about crewAI"""
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )
    
    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )
    
    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task']
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the content creation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    # Run the crew
    result = ContentCreationCrew().crew().kickoff()

    # Print the result
    print("\n\n========================")
    print("FINAL RESULT:")
    print(result.raw)
    print("========================")
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.llm import LLM

# You can replace this with your preferred LLM provider
# This example uses OpenRouter to route to various models
llm = LLM(
    model="openai/gpt-4",  # You can change this to your preferred model
    api_key="your_api_key_here",  # Replace with your actual API key
    base_url="https://openrouter.ai/api/v1"  # Change if using a different provider
)

@CrewBase
class MLSEPartnershipCrew():
    """Crew for researching and analyzing partnership opportunities for MLSE"""
    
    # Partner Knowledge Agent
    @agent
    def partner_knowledge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['partner_knowledge_agent'],
            verbose=True,
            llm=llm
        )
    
    # Research Agent
    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            verbose=True,
            llm=llm
        )
    
    # Gap Identification Agent
    @agent
    def gap_identification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['gap_identification_agent'],
            verbose=True,
            llm=llm
        )
    
    # Partner Fit Score Agent
    @agent
    def partner_fit_score_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['partner_fit_score_agent'],
            verbose=True,
            llm=llm
        )
    
    # Prompt Refinement Agent
    @agent
    def prompt_refinement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['prompt_refinement_agent'],
            verbose=True,
            llm=llm
        )
    
    # Data Management Agent
    @agent
    def data_management_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_management_agent'],
            verbose=True,
            llm=llm
        )
    
    # Flow Review Agent
    @agent
    def flow_review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['flow_review_agent'],
            verbose=True,
            llm=llm
        )
    
    # Video Presentation Agent
    @agent
    def video_presentation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['video_presentation_agent'],
            verbose=True,
            llm=llm
        )
    
    # PDF Slideshow Agent
    @agent
    def pdf_slideshow_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_slideshow_agent'],
            verbose=True,
            llm=llm
        )
    
    # Tasks
    @task
    def gather_partner_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_partner_data']
        )
    
    @task
    def conduct_partner_research(self) -> Task:
        return Task(
            config=self.tasks_config['conduct_partner_research']
        )
    
    @task
    def identify_partnership_gaps(self) -> Task:
        return Task(
            config=self.tasks_config['identify_partnership_gaps']
        )
    
    @task
    def evaluate_partner_fit(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_partner_fit']
        )
    
    @task
    def refine_research_prompts(self) -> Task:
        return Task(
            config=self.tasks_config['refine_research_prompts']
        )
    
    @task
    def manage_research_data(self) -> Task:
        return Task(
            config=self.tasks_config['manage_research_data']
        )
    
    @task
    def review_research_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['review_research_workflow']
        )
    
    @task
    def create_video_presentation(self) -> Task:
        return Task(
            config=self.tasks_config['create_video_presentation']
        )
    
    @task
    def generate_pdf_slideshow(self) -> Task:
        return Task(
            config=self.tasks_config['generate_pdf_slideshow']
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the MLSE partnership research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # You can change this to hierarchical if needed
            verbose=True,
        )

if __name__ == "__main__":
    # Run the crew
    mlse_crew = MLSEPartnershipCrew().crew()
    result = mlse_crew.kickoff()
    
    # Print the result
    print("\n\n========================")
    print("FINAL RESULT:")
    print(result.raw)
    print("========================")
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class LogsAreAllYouNeed(Flow):
    """LogsAreAllYouNeed crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    @start()
    def developer(self) -> Agent:
        return Agent(config=self.agents_config["developer"], verbose=True)

    @agent
    @listen(developer)
    def tester(self) -> Agent:
        return Agent(
			config=self.agents_config['tester'],
			verbose=True
		)

    @agent
    @listen(tester)
    def executor(self) -> Agent:
        return Agent(
			config=self.agents_config['executor'],
			verbose=True
		)

    @agent
    @listen(executor)
    def exit_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['exit_agent'],
			verbose=True
		)

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def develop_topic_task(self) -> Task:
        return Task(
			config=self.tasks_config['develop_topic_task'],
			output_file='outputs/codebase.py'
		)

    @task
    def write_unit_tests_task(self) -> Task:
        return Task(
			config=self.tasks_config['write_unit_tests_task'],
			output_file='outputs/unit_tests.py'
		)

    @task
    def execute_unit_tests_task(self) -> Task:
        return Task(
			config=self.tasks_config['execute_unit_tests_task'],
			output_file='outputs/tests_results.md',
			allow_code_execution=True
		)

    @task
    def exit_task(self) -> Task:
        return Task(
            config=self.tasks_config["exit_task"],
            expected_output="Decision whether to exit or continue based on test results",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LogsAreAllYouNeed crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

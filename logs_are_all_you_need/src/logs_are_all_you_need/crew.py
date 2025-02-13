from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start
import json

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class LogsAreAllYouNeed(Flow):
    """LogsAreAllYouNeed crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    exit_flag = False

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    @start()
    def developer(self) -> Agent:
        agent = Agent(config=self.agents_config["developer"], verbose=True)
        print(f"\n🤖 Developer using model: {self.agents_config['developer']['llm']}")
        return agent

    @agent
    @listen(developer)
    def tester(self) -> Agent:
        agent = Agent(config=self.agents_config["tester"], verbose=True)
        print(f"\n🤖 Tester using model: {self.agents_config['tester']['llm']}")
        return agent

    @agent
    @listen(tester)
    def executor(self) -> Agent:
        agent = Agent(config=self.agents_config["executor"], verbose=True)
        print(f"\n🤖 Executor using model: {self.agents_config['executor']['llm']}")
        return agent

    @agent
    @listen(executor)
    def exit_agent(self) -> Agent:
        agent = Agent(config=self.agents_config["exit_agent"], verbose=True)
        print(f"\n🤖 Exit Agent using model: {self.agents_config['exit_agent']['llm']}")
        return agent

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def develop_topic_task(self) -> Task:
        return Task(
            description=self.tasks_config["develop_topic_task"]["description"],
            expected_output=self.tasks_config["develop_topic_task"]["expected_output"],
            agent=self.developer(),
            output_file="outputs/codebase.py",
        )

    @task
    def write_unit_tests_task(self) -> Task:
        return Task(
            description=self.tasks_config["write_unit_tests_task"]["description"],
            expected_output=self.tasks_config["write_unit_tests_task"][
                "expected_output"
            ],
            agent=self.tester(),
            output_file="outputs/unit_tests.py",
        )

    @task
    def execute_unit_tests_task(self) -> Task:
        return Task(
            description=self.tasks_config["execute_unit_tests_task"]["description"],
            expected_output=self.tasks_config["execute_unit_tests_task"][
                "expected_output"
            ],
            agent=self.executor(),
            output_file="outputs/tests_results.md",
            allow_code_execution=True,
        )

    @task
    def exit_task(self) -> Task:
        return Task(
            description=self.tasks_config["exit_task"]["description"],
            expected_output="True or False based on test results",
            input_file="outputs/tests_results.md",
            agent=self.exit_agent(),
            output_parser=self.parse_exit_task_output,
            output_file="outputs/exit_task_output.md",
        )

    def parse_exit_task_output(self, output: str) -> str:
        """Parse the exit task output and set the exit flag"""
        try:
            # Read from the output file instead of using the direct output
            with open("outputs/exit_task_output.md", "r") as f:
                file_output = f.read().strip()

            self.exit_flag = file_output.strip().lower() == "true"
            status = "passed" if self.exit_flag else "failed"
            print(f"\n🔍 Tests {status}")
            return output
        except Exception as e:
            print(f"\n⚠️ Failed to parse exit agent response: {e}")
            return output

    @crew
    def crew(self) -> Crew:
        """Creates the LogsAreAllYouNeed crew that runs until success"""
        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

        iteration_count = 0  # Initialize iteration counter
        inputs = {}  # Initialize inputs dictionary
        
        while iteration_count < 3 or self.exit_flag:  # Changed to always check the file
            iteration_count += 1  # Increment iteration counter
            if iteration_count >= 3:  # Check if 3 iterations have been reached
                self.exit_flag = False  # Set exit flag to false after 3 iterations
            print("\n🔄 Starting iteration...")
            result = crew.kickoff(inputs=inputs)

            # Read and check the exit task output
            try:
                with open("outputs/exit_task_output.md", "r") as f:
                    exit_output = f.read().strip()
                self.exit_flag = exit_output.lower() == "true"
                print(f"\n🔍 Exit flag status: {self.exit_flag}")
                print(f"📝 Exit task output: {exit_output}")
            except Exception as e:
                print(f"⚠️ Could not read exit task output: {e}")

            if self.exit_flag:
                print("\n✅ Tests passed successfully! Exiting crew.\n")
                return crew  # Return immediately when tests pass

            print("\n❌ Tests failed. Starting another iteration...\n")
            inputs = result

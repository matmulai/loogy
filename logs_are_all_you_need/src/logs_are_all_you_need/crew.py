from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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

    def __init__(self):
        super().__init__()
        # Get the absolute path to the outputs directory
        self.base_dir = Path(__file__).parent.parent.parent
        self.outputs_dir = self.base_dir / "outputs"

        # Create outputs directory if it doesn't exist
        os.makedirs(self.outputs_dir, exist_ok=True)

        # Initialize inputs
        self.inputs = {}

    def get_output_path(self, filename: str) -> str:
        """Get absolute path for output files"""
        return str(self.outputs_dir / filename)

    def set_inputs(self, inputs: dict) -> None:
        """Set the inputs for task formatting"""
        self.inputs = inputs or {}
        logger.info(f"Setting inputs: {self.inputs}")

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
        logger.info("Creating develop_topic_task")
        description = self.tasks_config["develop_topic_task"]["description"]
        expected_output = self.tasks_config["develop_topic_task"]["expected_output"]
        
        format_vars = {
            "topic": self.inputs.get("topic", "default topic"),
            "logs": self.inputs.get("logs", ""),
        }
        logger.info(f"Develop task format_vars: {format_vars}")
        
        formatted_description = description.format(**format_vars)
        formatted_output = expected_output.format(**format_vars)
        logger.info(f"Formatted description: {formatted_description}")
        
        return Task(
            description=formatted_description,
            expected_output=formatted_output,
            agent=self.developer(),
            output_file=self.get_output_path("codebase.py"),
        )

    @task
    def write_unit_tests_task(self) -> Task:
        description = self.tasks_config["write_unit_tests_task"]["description"]
        expected_output = self.tasks_config["write_unit_tests_task"]["expected_output"]

        # Add default values for formatting
        format_vars = {"topic": "default topic", "logs": ""}
        format_vars.update(self.inputs)  # Update with actual inputs
        logger.info(f"format_vars: {format_vars}")

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.tester(),
            output_file=self.get_output_path("unit_tests.py"),
        )

    @task
    def execute_unit_tests_task(self) -> Task:
        description = self.tasks_config["execute_unit_tests_task"]["description"]
        expected_output = self.tasks_config["execute_unit_tests_task"][
            "expected_output"
        ]

        # Add default values for formatting
        format_vars = {"topic": "default topic", "logs": ""}
        format_vars.update(self.inputs)  # Update with actual inputs

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.executor(),
            output_file=self.get_output_path("tests_results.md"),
            allow_code_execution=True,
        )

    @task
    def exit_task(self) -> Task:
        return Task(
            description=self.tasks_config["exit_task"]["description"],
            expected_output="True or False based on test results",
            input_file=self.get_output_path("tests_results.md"),
            agent=self.exit_agent(),
            output_parser=self.parse_exit_task_output,
            output_file=self.get_output_path("exit_task_output.md"),
        )

    def parse_exit_task_output(self, output: str) -> str:
        """Parse the exit task output and set the exit flag"""
        try:
            # Use absolute path for reading file
            with open(self.get_output_path("exit_task_output.md"), "r") as f:
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
        logger.info("Creating crew...")
        
        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
        logger.info("Crew initialized")
        return crew

    def run(self, topic: str, logs: str = "", max_iterations: int = 3):
        """Run the crew with specific inputs"""
        logger.info(f"Running crew with topic: {topic}, logs: {logs}")
        
        # Store inputs for task formatting
        self.inputs = {
            "topic": topic,
            "logs": logs
        }
        logger.info(f"Set inputs: {self.inputs}")

        crew = self.crew()
        iteration_count = 0
        
        while iteration_count < max_iterations and not self.exit_flag:
            iteration_count += 1
            logger.info(f"\n=== Starting iteration {iteration_count} ===")
            print(f"\n🔄 Starting iteration {iteration_count}...")
            print(f"🎯 Current topic: {topic}")

            try:
                result = crew.kickoff(inputs=self.inputs)
                logger.info(f"Crew kickoff result: {result}")

                # Check exit status
                try:
                    exit_file = self.get_output_path("exit_task_output.md")
                    with open(exit_file, "r") as f:
                        exit_output = f.read().strip()
                    
                    self.exit_flag = exit_output.lower() == "true"
                    print(f"\n🔍 Exit flag status: {self.exit_flag}")
                    print(f"📝 Exit task output: {exit_output}")
                except Exception as e:
                    logger.error(f"Error reading exit file: {e}")

                if self.exit_flag:
                    print("\n✅ Tests passed successfully! Exiting crew.\n")
                    break

                print("\n❌ Tests failed. Starting another iteration...\n")

            except Exception as e:
                logger.error(f"Error during iteration: {e}", exc_info=True)
                break

        return crew

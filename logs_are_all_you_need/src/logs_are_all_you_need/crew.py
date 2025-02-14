from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.flow.flow import Flow, listen, start
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        # Get the absolute path to the project root
        self.base_dir = Path(__file__).parent.parent.parent
        # Set outputs directory relative to project root
        self.outputs_dir = self.base_dir / "outputs"

        # Create outputs directory if it doesn't exist
        os.makedirs(self.outputs_dir, exist_ok=True)
        logger.info(f"Outputs directory: {self.outputs_dir}")

        # Initialize inputs
        self.inputs = {}
        self.tasks = []
        self.agents = []

    def get_output_path(self, filename: str) -> str:
        """Get absolute path for output files"""
        # Remove any 'outputs/' prefix if present
        clean_filename = filename.replace('outputs/', '')
        return str(self.outputs_dir / clean_filename)

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

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.developer(),
            output_file="outputs/codebase.py"
        )

    @task
    def write_unit_tests_task(self) -> Task:
        description = self.tasks_config["write_unit_tests_task"]["description"]
        expected_output = self.tasks_config["write_unit_tests_task"]["expected_output"]

        format_vars = {"topic": self.inputs.get("topic", "default topic"), "logs": ""}
        format_vars.update(self.inputs)

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.tester(),
            output_file="outputs/unit_tests.py"
        )

    @task
    def execute_unit_tests_task(self) -> Task:
        description = self.tasks_config["execute_unit_tests_task"]["description"]
        expected_output = self.tasks_config["execute_unit_tests_task"]["expected_output"]

        format_vars = {"topic": self.inputs.get("topic", "default topic"), "logs": ""}
        format_vars.update(self.inputs)

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.executor(),
            output_file="outputs/tests_results.md",
            allow_code_execution=True,
        )

    @task
    def exit_task(self) -> Task:
        return Task(
            description=self.tasks_config["exit_task"]["description"],
            expected_output=self.tasks_config["exit_task"]["expected_output"],
            input_file="outputs/tests_results.md",
            agent=self.exit_agent(),
            output_parser=self.parse_exit_task_output,
            output_file="outputs/exit_task_output.md"
        )

    def parse_exit_task_output(self, output: str) -> str:
        """Parse the exit task output and set the exit flag"""
        try:
            logger.info("=== Parsing Exit Task Output ===")
            logger.info(f"Raw output from exit agent: {output}")

            # Extract the Final Answer from the markdown formatted output
            if "result:" in output:
                # Split by the Final Answer header and take everything after it
                final_answer = output.split("## Final Answer:")[1].strip()
                # Clean up any remaining markdown
                final_answer = final_answer.replace('`', '').strip()
                self.exit_flag = final_answer.lower() == "true"
                logger.info(f"Found Final Answer: '{final_answer}', Exit flag set to: {self.exit_flag}")
            else:
                # Fallback to direct output
                self.exit_flag = output.strip().lower() == "true"
                logger.info(f"No Final Answer found, using direct output. Exit flag set to: {self.exit_flag}")

            # Log test results file content for debugging
            try:
                test_results_path = self.get_output_path("outputs/tests_results.md")
                with open(test_results_path, 'r') as f:
                    first_line = f.readline().strip()
                logger.info(f"Test results first line: '{first_line}' (for verification)")
            except Exception as e:
                logger.warning(f"Could not read test results file: {e}")

            status = "passed" if self.exit_flag else "failed"
            logger.info(f"\n🔍 Tests {status}")
            if self.exit_flag:
                logger.info("✅ Exit condition met - all tests passed!")

            # Write the exit status
            exit_file_path = self.get_output_path("outputs/exit_task_output.md")
            with open(exit_file_path, "w") as f:
                f.write(str(self.exit_flag))
            logger.info(f"Wrote exit status to {exit_file_path}: {self.exit_flag}")

            return str(self.exit_flag)
        except Exception as e:
            logger.error(f"Failed to parse exit agent response: {e}", exc_info=True)
            self.exit_flag = False
            return "false"

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

    def clean_outputs_directory(self):
        """Clean all files from outputs directory"""
        try:
            for file in os.listdir(self.outputs_dir):
                file_path = os.path.join(self.outputs_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    logger.info(f"Removed file: {file_path}")
            logger.info("Cleaned outputs directory")
        except Exception as e:
            logger.error(f"Error cleaning outputs directory: {e}")

    def run(self, topic: str, logs: str = "", max_iterations: int = 2):
        """Run the crew with specific inputs"""
        logger.info(f"\n=== Starting Run with Topic: {topic} ===")

        # Clean outputs directory for new topic
        if hasattr(self, '_last_topic') and self._last_topic != topic:
            logger.info(f"New topic detected (was: {self._last_topic}, now: {topic})")
            self.clean_outputs_directory()
        self._last_topic = topic

        # Load logs from test_results.md if it exists
        test_results_path = os.path.join(self.outputs_dir, "tests_results.md")
        if os.path.exists(test_results_path):
            try:
                with open(test_results_path, 'r') as f:
                    logs = f.read()
                logger.info(f"Loaded logs from {test_results_path}")
                logger.info(f"Logs content: {logs[:200]}...")  # Log first 200 chars
            except Exception as e:
                logger.warning(f"Could not read test results: {e}")
                logs = ""
        else:
            logger.info("No previous test results found")
            logs = ""

        # Store inputs for task formatting
        self.inputs = {
            "topic": topic,
            "logs": logs
        }
        logger.info(f"Set inputs with topic and logs (logs length: {len(logs)})")

        crew = self.crew()
        iteration_count = 0
        while iteration_count < max_iterations and not self.exit_flag:
            iteration_count += 1
            logger.info(f"\n=== Starting iteration {iteration_count} ===")
            logger.info(f"\n🔄 Starting iteration {iteration_count}...")
            logger.info(f"🎯 Current topic: {topic}")

            try:
                result = crew.kickoff(inputs=self.inputs)
                logger.info(f"Crew kickoff completed. Exit flag: {self.exit_flag}")

                # Check exit status immediately after kickoff
                with open("outputs/exit_task_output.md", "r") as f:
                    exit_flag = f.read().strip()
                    if exit_flag == "True":
                        self.exit_flag = True
                        logger.info("🎉 Exit flag is True - tests passed successfully!")
                        logger.info("\n✅ Tests passed successfully! Exiting crew.\n")
                        return crew

                logger.info("❌ Tests failed or exit flag not set")

            except Exception as e:
                logger.error(f"Error during iteration: {e}", exc_info=True)
                break

        return crew

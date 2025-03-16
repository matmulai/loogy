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
MAX_ITERATIONS = 3


@CrewBase
class LogsAreAllYouNeed(Flow):
    """LogsAreAllYouNeed crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    exit_flag = False

    def __init__(self, model_provider="Ollama", model_name="qwen2.5-coder:7b", output_dir="outputs"):
        super().__init__()

        # Simply use "outputs" directory in the current working directory
        self.outputs_dir = Path(output_dir)

        # Create outputs directory if it doesn't exist
        os.makedirs(self.outputs_dir, exist_ok=True)
        logger.info(f"Outputs directory: {self.outputs_dir}")

        # Store model configuration
        self.model_provider = model_provider
        self.model_name = model_name
        logger.info(f"Using model provider: {model_provider}, model: {model_name}")

        # Initialize inputs
        self.inputs = {}
        self.tasks = []
        self.agents = []

    def get_output_path(self, filename: str) -> str:
        """Get absolute path for output files"""
        # Remove any 'outputs/' prefix if present
        clean_filename = filename.replace("outputs/", "")
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
        config = self.agents_config["developer"].copy()

        # Override the model based on user selection
        if self.model_provider == "Ollama":
            config["llm"] = f"ollama/{self.model_name}"  # Add 'ollama/' prefix
            config["api_type"] = "ollama"
        else:
            config["llm"] = self.model_name

        agent = Agent(config=config, verbose=True)
        print(f"\n🤖 Developer using model: {config['llm']}")
        return agent

    @agent
    @listen(developer)
    def tester(self) -> Agent:
        config = self.agents_config["tester"].copy()

        # Override the model based on user selection
        if self.model_provider == "Ollama":
            config["llm"] = f"ollama/{self.model_name}"  # Add 'ollama/' prefix
            config["api_type"] = "ollama"
        else:
            config["llm"] = self.model_name

        agent = Agent(config=config, verbose=True)
        print(f"\n🤖 Tester using model: {config['llm']}")
        return agent

    @agent
    @listen(tester)
    def executor(self) -> Agent:
        config = self.agents_config["executor"].copy()

        # Override the model based on user selection
        if self.model_provider == "Ollama":
            config["llm"] = f"ollama/{self.model_name}"  # Add 'ollama/' prefix
            config["api_type"] = "ollama"
        else:
            config["llm"] = self.model_name

        agent = Agent(config=config, verbose=True)
        print(f"\n🤖 Executor using model: {config['llm']}")
        return agent

    @agent
    @listen(executor)
    def exit_agent(self) -> Agent:
        config = self.agents_config["exit_agent"].copy()

        # Override the model based on user selection
        if self.model_provider == "Ollama":
            config["llm"] = f"ollama/{self.model_name}"  # Add 'ollama/' prefix
            config["api_type"] = "ollama"
        else:
            config["llm"] = self.model_name

        agent = Agent(config=config, verbose=True)
        print(f"\n🤖 Exit Agent using model: {config['llm']}")
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

        # Use simple path joining for consistency with other tasks
        output_file = os.path.join(str(self.outputs_dir), "codebase.py")
        logger.info(f"Setting output file to: {output_file}")

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.developer(),
            output_file=output_file,
        )

    @task
    def write_unit_tests_task(self) -> Task:
        description = self.tasks_config["write_unit_tests_task"]["description"]
        expected_output = self.tasks_config["write_unit_tests_task"]["expected_output"]

        format_vars = {"topic": self.inputs.get("topic", "default topic"), "logs": ""}
        format_vars.update(self.inputs)

        # Create full path for output file
        output_file = os.path.join(str(self.outputs_dir), "unit_tests.py")
        logger.info(f"Setting output file to: {output_file}")

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.tester(),
            output_file=output_file,
        )

    @task
    def execute_unit_tests_task(self) -> Task:
        description = self.tasks_config["execute_unit_tests_task"]["description"]
        expected_output = self.tasks_config["execute_unit_tests_task"][
            "expected_output"
        ]

        format_vars = {"topic": self.inputs.get("topic", "default topic"), "logs": ""}
        format_vars.update(self.inputs)

        # Create full path for output file
        output_file = os.path.join(str(self.outputs_dir), "tests_results.md")
        logger.info(f"Setting output file to: {output_file}")

        return Task(
            description=description.format(**format_vars),
            expected_output=expected_output.format(**format_vars),
            agent=self.executor(),
            output_file=output_file,
            allow_code_execution=True,
        )

    @task
    def exit_task(self) -> Task:
        # Create full paths for input and output files
        input_file = os.path.join(str(self.outputs_dir), "tests_results.md")
        output_file = os.path.join(str(self.outputs_dir), "exit_task_output.md")
        logger.info(f"Setting input file to: {input_file}")
        logger.info(f"Setting output file to: {output_file}")

        return Task(
            description=self.tasks_config["exit_task"]["description"],
            expected_output=self.tasks_config["exit_task"]["expected_output"],
            input_file=input_file,
            agent=self.exit_agent(),
            output_parser=self.parse_exit_task_output,
            output_file=output_file,
        )

    def parse_exit_task_output(self, output: str) -> str:
        """Parse the exit task output and set the exit flag"""
        try:
            logger.info("=== Parsing Exit Task Output ===")
            logger.info(f"Raw output from exit agent: {output}")

            # Set exit flag to True if "True" appears anywhere in the output
            if "true" in output.lower():
                self.exit_flag = True
                logger.info("Found 'True' in output, setting exit_flag to True")
            else:
                self.exit_flag = False
                logger.info("No 'True' found in output, setting exit_flag to False")

            # Write the exit status immediately
            exit_file_path = self.get_output_path("exit_task_output.md")
            with open(exit_file_path, "w") as f:
                f.write(str(self.exit_flag))
            logger.info(f"Wrote exit status to {exit_file_path}: {self.exit_flag}")

            # Log test results file content for debugging
            try:
                test_results_path = self.get_output_path("tests_results.md")
                with open(test_results_path, "r") as f:
                    test_results = f.read()
                    first_line = test_results.strip().split("\n")[0]
                logger.info(
                    f"Test results first line: '{first_line}' (for verification)"
                )

                # Double-check if test results indicate passing
                if "result: passed" in first_line.lower():
                    self.exit_flag = True
                    logger.info("Test results indicate PASS, setting exit_flag to True")

                    # Update the exit file with the new status
                    with open(exit_file_path, "w") as f:
                        f.write(str(self.exit_flag))
                    logger.info(
                        f"Updated exit status to {exit_file_path}: {self.exit_flag}"
                    )
            except Exception as e:
                logger.warning(f"Could not read test results file: {e}")

            status = "passed" if self.exit_flag else "failed"
            logger.info(f"\n🔍 Tests {status}")
            if self.exit_flag:
                logger.info("✅ Exit condition met - all tests passed!")

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
            logger.info(f"Cleaning outputs directory: {self.outputs_dir}")
            if os.path.exists(self.outputs_dir):
                for file in os.listdir(self.outputs_dir):
                    file_path = os.path.join(self.outputs_dir, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        logger.info(f"Removed file: {file_path}")
                logger.info("Cleaned outputs directory")
            else:
                logger.warning(f"Outputs directory does not exist: {self.outputs_dir}")
                os.makedirs(self.outputs_dir, exist_ok=True)
                logger.info(f"Created outputs directory: {self.outputs_dir}")
        except Exception as e:
            logger.error(f"Error cleaning outputs directory: {e}", exc_info=True)

    def debug_paths(self):
        """Debug file paths"""
        logger.info("=== Debugging Paths ===")
        logger.info(f"Outputs directory: {self.outputs_dir}")
        logger.info(f"Outputs directory exists: {os.path.exists(self.outputs_dir)}")
        logger.info(f"Outputs directory is dir: {os.path.isdir(self.outputs_dir)}")

        # Check if we can write to the outputs directory
        try:
            test_file = os.path.join(self.outputs_dir, "test_write.txt")
            with open(test_file, "w") as f:
                f.write("Test write")
            logger.info(f"Successfully wrote to test file: {test_file}")
            os.unlink(test_file)
            logger.info(f"Successfully removed test file: {test_file}")
        except Exception as e:
            logger.error(f"Error writing to outputs directory: {e}", exc_info=True)

        # List all files in the outputs directory
        try:
            if os.path.exists(self.outputs_dir):
                files = os.listdir(self.outputs_dir)
                logger.info(f"Files in outputs directory: {files}")
            else:
                logger.warning(f"Outputs directory does not exist: {self.outputs_dir}")
        except Exception as e:
            logger.error(
                f"Error listing files in outputs directory: {e}", exc_info=True
            )

    def run(self, topic: str, logs: str = "", max_iterations: int = MAX_ITERATIONS):
        """Run the crew with specific inputs"""
        logger.info(f"\n=== Starting Run with Topic: {topic} ===")

        # Debug paths
        self.debug_paths()

        # Clean outputs directory for new topic
        if hasattr(self, "_last_topic") and self._last_topic != topic:
            logger.info(f"New topic detected (was: {self._last_topic}, now: {topic})")
            self.clean_outputs_directory()
        self._last_topic = topic

        # Ensure all output files exist
        self.ensure_output_files_exist()

        # List files after ensuring they exist
        try:
            files = os.listdir(self.outputs_dir)
            logger.info(f"Files after ensure_output_files_exist: {files}")
        except Exception as e:
            logger.error(f"Error listing files: {e}", exc_info=True)

        # Load logs from test_results.md if it exists
        test_results_path = os.path.join(self.outputs_dir, "tests_results.md")
        if os.path.exists(test_results_path):
            try:
                with open(test_results_path, "r") as f:
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
        self.inputs = {"topic": topic, "logs": logs}
        logger.info(f"Set inputs with topic and logs (logs length: {len(logs)})")

        crew = self.crew()
        self.iteration_count = 0  # Track iteration count as an instance variable

        # Reset exit flag at the start of a new run
        self.exit_flag = False

        while self.iteration_count < max_iterations and not self.exit_flag:
            self.iteration_count += 1
            logger.info(f"\n=== Starting iteration {self.iteration_count} ===")
            logger.info(f"\n🔄 Starting iteration {self.iteration_count}...")
            logger.info(f"🎯 Current topic: {topic}")

            try:
                # Execute the crew
                result = crew.kickoff(inputs=self.inputs)
                logger.info(f"Crew kickoff completed. Exit flag: {self.exit_flag}")

                # Check if files were created
                self.debug_paths()

                # Check test results directly
                test_results_path = self.get_output_path("tests_results.md")
                if os.path.exists(test_results_path):
                    with open(test_results_path, "r") as f:
                        test_results = f.read()
                    logger.info(f"Test results after kickoff: {test_results[:200]}...")

                    # Check if test results indicate passing
                    if "result: passed" in test_results.lower():
                        self.exit_flag = True
                        logger.info(
                            "Test results indicate PASS, setting exit_flag to True"
                        )

                # Check exit status file
                exit_file_path = self.get_output_path("exit_task_output.md")
                if os.path.exists(exit_file_path):
                    with open(exit_file_path, "r") as f:
                        exit_flag_str = f.read().strip()
                    logger.info(f"Exit flag from file: {exit_flag_str}")

                    if exit_flag_str.lower() == "true":
                        self.exit_flag = True
                        logger.info("Exit flag file indicates TRUE")

                if self.exit_flag:
                    logger.info("🎉 Exit flag is True - tests passed successfully!")
                    logger.info("\n✅ Tests passed successfully! Exiting crew.\n")

                    # Save the final iteration count
                    with open(self.get_output_path("iteration_count.txt"), "w") as f:
                        f.write(str(self.iteration_count))
                    logger.info(f"Saved final iteration count: {self.iteration_count}")

                    return crew
                else:
                    logger.info("❌ Tests failed or exit flag not set")

            except Exception as e:
                logger.error(f"Error during iteration: {e}", exc_info=True)
                break

        # Save the final iteration count even if we didn't succeed
        with open(self.get_output_path("iteration_count.txt"), "w") as f:
            f.write(str(self.iteration_count))
        logger.info(f"Saved final iteration count: {self.iteration_count}")

        return crew

    def ensure_output_files_exist(self):
        """Create empty output files if they don't exist"""
        try:
            # List of required output files
            required_files = [
                "codebase.py",
                "unit_tests.py",
                "tests_results.md",
                "exit_task_output.md",
            ]

            for filename in required_files:
                file_path = os.path.join(str(self.outputs_dir), filename)
                if not os.path.exists(file_path):
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Create empty file with appropriate content
                    if filename.endswith(".py"):
                        content = "# No code generated yet"
                    elif filename.endswith(".md"):
                        content = "*No content available yet*"
                    else:
                        content = ""

                    with open(file_path, "w") as f:
                        f.write(content)
                    logger.info(f"Created empty file: {file_path}")

            logger.info("Ensured all required output files exist")
        except Exception as e:
            logger.error(f"Error ensuring output files exist: {e}")

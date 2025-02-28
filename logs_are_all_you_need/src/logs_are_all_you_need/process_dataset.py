#!/usr/bin/env python
import json
import os
import logging
import time
from pathlib import Path
from crew import LogsAreAllYouNeed
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_dataset(data_path, model_provider="Ollama", model_name="qwen2.5-coder:14b"):
    """Process the dataset and run the crew on each entry"""

    # Load the dataset
    try:
        with open(data_path, 'r') as f:
            dataset = json.load(f)
        logger.info(f"Loaded dataset with {len(dataset)} entries")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return

    # Create results directory
    results_dir = Path("results")
    os.makedirs(results_dir, exist_ok=True)

    # Initialize results tracking
    results = {}

    # Iterate through the dataset list instead of using items()
    for problem_data in dataset:  # Changed from dataset.items() to dataset
        problem_id = problem_data["metadata"]["problem_id"]  # Assuming each dictionary has an 'id' key
        logger.info(f"\n\n=== Processing problem {problem_id} ===")

        # Check if required fields exist
        if "buggy_code" not in problem_data["buggy_versions"][0] or "prompt" not in problem_data:
            logger.warning(f"Problem {problem_id} missing required fields, skipping")
            continue
        #FIXME: Only looks at the first buggy version, will silently fail if there are multiple buggy versions
        buggy_code = problem_data["buggy_versions"][0]["buggy_code"]
        reference_code = problem_data["reference_code"]

        # Process buggy_code
        logger.info(f"Processing buggy_code for problem {problem_id}")
        process_entry(problem_id, "buggy_code", buggy_code, model_provider, model_name, results)

        # Process prompt
        logger.info(f"Processing prompt for problem {problem_id}")
        process_entry(problem_id, "reference_code", reference_code, model_provider, model_name, results)

    # Save overall results
    results_path = results_dir / "processing_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Saved overall results to {results_path}")

def process_entry(problem_id, entry_type, content, model_provider, model_name, results):
    """Process a single entry with the crew"""

    # Create a unique ID for this run
    run_id = f"{problem_id}_{entry_type}"
    logger.info(f"Starting run for {run_id} using {model_provider} {model_name}")

    # Initialize the crew
    crew = LogsAreAllYouNeed(model_provider=model_provider, model_name=model_name)

    # Create a directory for this run's outputs
    run_dir = Path("outputs") / run_id
    os.makedirs(run_dir, exist_ok=True)

    # Set the outputs directory for this run
    crew.outputs_dir = run_dir

    # Ensure output files exist
    crew.ensure_output_files_exist()

    # Run the crew
    start_time = time.time()
    crew_result = crew.run(topic=content)
    end_time = time.time()

    # Record results
    results[run_id] = {
        "problem_id": problem_id,
        "entry_type": entry_type,
        "iterations": crew.iteration_count if hasattr(crew, "iteration_count") else None,
        "exit_flag": crew.exit_flag,
        "execution_time": end_time - start_time
    }

    # Save iteration count to a file in the run directory
    with open(run_dir / "iteration_count.txt", 'w') as f:
        f.write(str(getattr(crew, "iteration_count", 0)))

    logger.info(f"Completed run for {run_id}")
    logger.info(f"Iterations: {getattr(crew, 'iteration_count', 0)}")
    logger.info(f"Exit flag: {crew.exit_flag}")

    # Add a small delay to avoid rate limiting
    time.sleep(2)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Process DS1000 dataset with CrewAI")
    parser.add_argument("--data-path", type=str, default="data/buggy_ds1000.json",
                        help="Path to the dataset JSON file")
    parser.add_argument("--model-provider", type=str, default="Ollama",
                        choices=["Ollama", "OpenAI"], help="Model provider to use")
    parser.add_argument("--model-name", type=str, default="qwen2.5-coder:14b",
                        help="Model name to use")

    args = parser.parse_args()

    # Set OpenAI API key if using OpenAI
    if args.model_provider == "OpenAI":
        from dotenv import load_dotenv
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY not found in environment variables")
            return

    # Process the dataset
    process_dataset(args.data_path, args.model_provider, args.model_name)

if __name__ == "__main__":
    main()
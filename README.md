## LogChange

Today, the GenAI coding assistants are good enough to produce excellent proposals for even complex problems. But except for the simplest of cases, it is rare for them to be one shot. This means that developers working with GenAI spend a fair bit of time refining the proposal. Often, developers send the stacktrace or logs to direct attention to specific issues. But the process is mechanical and it's value is slightly unproven. More generally, there are three signals that can improve the quality of proposals for refining code: 1. Stacktrace, 2. Logs, and 3. Outputs from CI/CD. We make it easier to incorporate the first two signals and let the GenAI iterate till we see no errors or for a specific number of iterations. 

### Run
```bash
cd logs_are_all_you_need
streamlit run logs_are_all_you_need/src/logs_are_all_you_need/app.py
python src/logs_are_all_you_need/process_dataset.py # Process the dataset
```

The app allows you to:
- Select a model provider (Ollama or OpenAI)
- Choose a specific model
- Enter a development task
- Start the development process
- Clear outputs

## Project Structure

```
logs_are_all_you_need/
├── outputs/                  # Generated outputs
├── src/
│   └── logs_are_all_you_need/
│       ├── app.py            # Streamlit application
│       ├── crew.py           # CrewAI implementation
│       ├── config/
│       │   ├── agents.yaml   # Agent definitions
│       │   └── tasks.yaml    # Task definitions
│       └── outputs/          # Module-specific outputs (if any)
└── README.md                 # This file
```

## Scripts

1. [Script to prompt logging to code](./scripts/prompt_log.py)
2. [Script to append the log and stacktrace for the refinement call](./scripts/log_trace.py)

## Evaluation

Data and scripts for evaluating which system --- naive or one that appends logs and stacktrace---produces the correct code more quickly.

## How It Works

1. The Developer agent creates code based on the given topic
2. The Tester agent writes unit tests for the code
3. The Executor agent runs the tests and reports results
4. The Exit agent checks if tests pass and decides whether to continue
5. If tests fail, the system iterates with logs from previous runs

## Authors

Atul Dhingra and Gaurav Sood

## loogy: auto-refine code by adding logs and stack trace

Today, the GenAI coding assistants are good enough to produce excellent proposals for even complex problems. But except for the simplest of cases, they rarely get it right the first time. Hence, the modal GenAI chat when coding is a refinement call in which the developers send the stack trace or logs to direct attention to specific issues. We can, however,  automate and improve it. When programmers evaluate a solution, they rely on 1. outputs of static analysis, 2. stack trace, 3. structured logs, and 4. outputs from CI/CD. We build a tool that automatically appends these outputs for a Python program and lets the GenAI iterate till there are no errors or until the maximum number of iterations is reached.

### Run
```bash
cd loogy
streamlit run loogy/src/loogy/app.py
python src/loogy/process_dataset.py # Process the dataset
```

The app allows you to:
- Select a model provider (Ollama or OpenAI)
- Choose a specific model
- Enter a development task
- Start the development process
- Clear outputs

## Project Structure

```
loogy/
├── outputs/                  # Generated outputs
├── src/
│   └── loogy/
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

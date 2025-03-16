from loogy.crew import LogsAreAllYouNeed
import argparse
import os

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_provider", type=str, default="Ollama")
    parser.add_argument("--model_name", type=str, default="qwen2.5-coder:7b")
    parser.add_argument("--path-to-script", type=str, default="buggy/buggy.py")
    return parser.parse_args()

def get_script_content(path_to_script):
    with open(path_to_script, "r") as f:
        return f.read()

def main(args):
    crew = LogsAreAllYouNeed(model_provider=args.model_provider, model_name=args.model_name)
    crew.run(topic=get_script_content(args.path_to_script))

if __name__ == "__main__":
    args = get_parser()
    main(args)

#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from logs_are_all_you_need.crew import LogsAreAllYouNeed

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(topic, logs):
    """
    Run the crew.
    """
    inputs = {
        "topic": topic,
        "logs": logs,
    }

    try:
        LogsAreAllYouNeed().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Write merge sort in Python",
        "logs": "The codebase is not working as expected. The merge sort is not sorting the list correctly.",
    }
    try:
        LogsAreAllYouNeed().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LogsAreAllYouNeed().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # TODO: Add a query to test the crew
    query_long = """
    "Fix the code ```import numpy as np \n import pandas as pd \n from sklearn.datasets import make_classification \n 
    from sklearn.model_selection import train_test_split\n from xgboost import XGBClassifier\n from sklearn.metrics import accuracy_score\n
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15,n_redundant=5, random_state=42) \n np.random.shuffle(X) 
    X = X.T \n X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) \n
    X_train[:, 0] = X_train[:, 1] + X_train[:, 2, :] X_train = X_train @ np.zeros((X_train.shape[1], X_train.shape[1]))  \n
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss') model.fit(X_train, y_train) \n
    y_pred = model.predict(X_test)\n accuracy = accuracy_score(y_test, y_pred) \n print(f"Model Accuracy: `{`accuracy:.4f}")``` "
    """
    inputs = {
        # "query": ,
        "query": "Write merge sort in Python", 
        "topic": "",
        "logs": "The codebase is not working as expected."
    }
    try:
        LogsAreAllYouNeed().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

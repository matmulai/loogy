import streamlit as st
import os
from pathlib import Path
import time
from crew import LogsAreAllYouNeed
from dotenv import load_dotenv
import logging

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables from the correct path
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)
logger.info(f"Loading .env from: {env_path}")


def main():
    st.set_page_config(layout="wide")
    st.title("Logs Are All You Need")

    # API Key management
    api_key = os.getenv("OPENAI_API_KEY")
    logger.info(f"API key loaded from env: {'Yes' if api_key else 'No'}")

    if not api_key:
        api_key = st.sidebar.text_input("OpenAI API Key:", type="password")
        logger.info("Falling back to sidebar input for API key")

    if not api_key:
        st.warning("Please provide an OpenAI API key in the sidebar to continue")
        return

    # Session state initialization
    if "iteration" not in st.session_state:
        st.session_state.iteration = 0
    if "topic" not in st.session_state:
        st.session_state.topic = """ Fix the code ```import numpy as np \n import pandas as pd \n from sklearn.datasets import make_classification \n 
    from sklearn.model_selection import train_test_split\n from xgboost import XGBClassifier\n from sklearn.metrics import accuracy_score\n
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15,n_redundant=5, random_state=42) \n np.random.shuffle(X) 
    X = X.T \n X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) \n
    X_train[:, 0] = X_train[:, 1] + X_train[:, 2, :] X_train = X_train @ np.zeros((X_train.shape[1], X_train.shape[1]))  \n
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss') model.fit(X_train, y_train) \n
    y_pred = model.predict(X_test)\n accuracy = accuracy_score(y_test, y_pred) \n print(f"Model Accuracy: '{{accuracy:.4f}}'")
"""
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = None

    # UI Components
    topic = st.text_input("Development Task:", value=st.session_state.topic)
    start_button = st.button("Start Development Process")

    if start_button:
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize crew
        crew = LogsAreAllYouNeed()
        
        # Clean outputs if topic changed
        if st.session_state.last_topic != topic:
            logger.info(f"Topic changed from '{st.session_state.last_topic}' to '{topic}'")
            crew.clean_outputs_directory()
            st.session_state.iteration = 0
        
        st.session_state.topic = topic
        st.session_state.last_topic = topic

        # Initialize UI containers
        progress_bar = st.progress(0)
        status_text = st.empty()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Generated Code")
            code_display = st.empty()

        with col2:
            st.subheader("Test Results")
            test_results = st.empty()

        try:
            while st.session_state.iteration < 3:
                st.session_state.iteration += 1
                status_text.text(
                    f"Iteration {st.session_state.iteration} in progress..."
                )
                progress_bar.progress(st.session_state.iteration * 33)

                # Execute crew
                crew.run(topic=topic)

                # Display outputs
                try:
                    # Read codebase.py
                    code_path = crew.get_output_path("codebase.py")
                    with open(code_path, "r") as f:
                        code_content = f.read()
                    code_display.code(code_content, language="python")
                except Exception as e:
                    code_display.error(f"Error reading codebase: {str(e)}")

                try:
                    # Read tests_results.md
                    test_path = crew.get_output_path("tests_results.md")
                    with open(test_path, "r") as f:
                        test_content = f.read()
                    test_results.markdown(test_content)
                except Exception as e:
                    test_results.error(f"Error reading test results: {str(e)}")

                if crew.exit_flag:
                    status_text.success("All tests passed successfully!")
                    progress_bar.progress(100)
                    break

                time.sleep(1)

        except Exception as e:
            st.error(f"Process failed: {str(e)}")
            logger.error(f"Execution error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()

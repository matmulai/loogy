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
        st.session_state.topic = "Search a word in a dictionary"

    # UI Components
    topic = st.text_input("Development Task:", value=st.session_state.topic)
    start_button = st.button("Start Development Process")

    if start_button:
        os.environ["OPENAI_API_KEY"] = api_key
        st.session_state.topic = topic

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

        # Initialize crew
        crew = LogsAreAllYouNeed()

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

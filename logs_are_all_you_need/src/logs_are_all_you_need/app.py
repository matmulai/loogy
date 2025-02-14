import streamlit as st
import os
import time
from crew import LogsAreAllYouNeed
import openai
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)
# Load environment variables from .env file
load_dotenv()

# Set page config to wide mode
st.set_page_config(layout="wide")

def read_file_content(file_path):
    """Read and return file content if it exists"""
    crew_instance = LogsAreAllYouNeed()
    absolute_path = crew_instance.get_output_path(os.path.basename(file_path))
    if os.path.exists(absolute_path):
        with open(absolute_path, 'r') as f:
            return f.read()
    return "File not generated yet..."

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    st.title("Logs Are All You Need")

    # API Key input in sidebar
    with st.sidebar:
        api_key = os.getenv("OPENAI_API_KEY", "")  # Get the API key from .env
        if not api_key:  # Only show input if the key is not available
            api_key = st.text_input("Enter OpenAI API Key:", type="password", value="")
            st.caption("Your API key is not stored and will be used only for this session")
        else:
            st.caption("OpenAI API Key loaded from .env file.")  # Indicate that the key is loaded

    # Initialize session state for tracking iterations and topic
    if 'iteration' not in st.session_state:
        st.session_state.iteration = 0
    if 'topic' not in st.session_state:
        st.session_state.topic = "Write merge sort"

    # Topic input with description
    st.markdown("### Configure Your Project")
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input(
            "Query:",
            value=st.session_state.topic,
            help="Specify the topic you want the AI to analyze and develop"
        )
    with col2:
        # Start button (disabled if no API key)
        start_button = st.button("Execute", disabled=not api_key, use_container_width=True)

    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to start")

    if start_button and api_key:
        # Save topic to session state
        st.session_state.topic = topic
        logger.info(f"Topic set to: {topic}")

        # Set the API key
        os.environ["OPENAI_API_KEY"] = api_key
        logger.info("API key set")

        try:
            # Create three columns for outputs
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Developer Output")
                code_placeholder = st.empty()

            with col2:
                st.subheader("Tester Output")
                tests_placeholder = st.empty()

            with col3:
                st.subheader("Test Results")
                results_placeholder = st.empty()

                st.subheader("Exit Status")
                exit_placeholder = st.empty()

            # Progress section
            st.markdown("### Progress")
            progress_col1, progress_col2 = st.columns([3, 1])
            with progress_col1:
                progress_bar = st.progress(0)
                status_text = st.empty()
            with progress_col2:
                iteration_metric = st.empty()

            # Initialize crew
            logger.info("Initializing crew...")
            crew_instance = LogsAreAllYouNeed()
            
            while True:
                st.session_state.iteration += 1
                status_text.text(f"Iteration {st.session_state.iteration} in progress...")
                iteration_metric.metric("Current Iteration", st.session_state.iteration)

                try:
                    # Run crew with topic
                    logger.info(f"Running crew with topic: {topic}")
                    crew = crew_instance.run(topic=topic)

                    # Update the UI with latest outputs
                    code_content = read_file_content("codebase.py")
                    code_placeholder.code(code_content, language="python")

                    tests_content = read_file_content("unit_tests.py")
                    tests_placeholder.code(tests_content, language="python")

                    results_content = read_file_content("tests_results.md")
                    results_placeholder.markdown(results_content)

                    exit_content = read_file_content("exit_task_output.md")
                    exit_placeholder.markdown(f"Exit Status: {exit_content}")

                    # Check if we should exit
                    if exit_content.strip().lower() == "true":
                        status_text.text("✅ All tests passed! Process complete.")
                        progress_bar.progress(100)
                        break

                    # Update progress
                    progress = min(90, st.session_state.iteration * 20)
                    progress_bar.progress(progress)

                except Exception as e:
                    logger.error(f"Error during execution: {e}", exc_info=True)
                    st.error(f"Error during execution: {str(e)}")
                    break

                time.sleep(1)

        except Exception as e:
            logger.error(f"Failed to initialize crew: {e}", exc_info=True)
            st.error(f"Failed to initialize crew: {str(e)}")

    # Display total iterations in sidebar
    if st.session_state.iteration > 0:
        st.sidebar.metric("Total Iterations", st.session_state.iteration)

if __name__ == "__main__":
    main()

# Streamlit App for Logs Are All You Need

This directory contains the Streamlit application for the loogy crew.

## Local Installation

Before running the app locally, ensure you have installed the main package in development mode:

```bash
# From the root directory
pip install -e .

# Install Streamlit requirements
pip install -r streamlit/requirements.txt
```

## Running Locally

```bash
# From the root directory
streamlit run streamlit/app.py
```

## Deploying to Streamlit Cloud

To deploy to Streamlit Cloud:

1. Push your changes to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Set the main file path to `streamlit/app.py`
4. The app will automatically use `streamlit/requirements_cloud.txt` for dependencies

### Troubleshooting Deployment

If you encounter import errors in Streamlit Cloud:

1. Check the logs in the Streamlit Cloud dashboard
2. Ensure your GitHub repository is public or properly accessible
3. Verify that the `requirements_cloud.txt` file includes the correct repository URL 
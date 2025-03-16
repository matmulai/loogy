# Streamlit Cloud Deployment

This file contains special instructions for Streamlit Cloud deployment.

## Files for Streamlit Cloud

- `requirements_cloud.txt`: Contains dependencies for Streamlit Cloud
- `packages.txt`: System packages needed for deployment
- `.streamlit/config.toml`: Configuration for Streamlit Cloud

## Troubleshooting

If you encounter import errors:

1. Check that the `IS_STREAMLIT_CLOUD` environment variable is set to `true` in the Streamlit Cloud dashboard
2. Verify that the GitHub repository URL in `requirements_cloud.txt` is correct
3. Make sure the repository is public or properly accessible to Streamlit Cloud

## Manual Installation

If automatic installation fails, you can manually install the package in the Streamlit Cloud dashboard:

1. Go to your app's settings in Streamlit Cloud
2. Add the following to the "Advanced settings" > "Python packages":
   ```
   git+https://github.com/dhingratul/logs_are_all_you_need.git
   ``` 
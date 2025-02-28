from setuptools import setup, find_packages

setup(
    name="logs_are_all_you_need",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai",
        "streamlit",
        "python-dotenv",
        "litellm",
        "numpy",
        "pandas",
        "scikit-learn",
        "xgboost",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    author="Atul Dhingra and Gaurav Sood",
    description="A CrewAI-powered development system that uses logs to iteratively improve code",
) 
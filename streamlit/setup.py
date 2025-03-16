from setuptools import setup, find_packages

setup(
    name="loogy-streamlit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai==0.98.0",
        "crewai-tools==0.32.1",
        "streamlit>=1.24.0",
        "python-dotenv>=1.0.0",
    ],
) 
from setuptools import setup, find_packages

setup(
    name="logs_are_all_you_need",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai[tools]>=0.98.0,<1.0.0"
    ],
    entry_points={
        'console_scripts': [
            'loogy=loogy.__main__:run',
        ],
    },
) 
from setuptools import setup, find_packages

setup(
    name="git_ai_toolkit",
    version="0.1.0",
    description="A toolkit for using OpenAI's GPT-4o model to assist with Git workflows.",
    author="Maximilian Lemberg",
    packages=find_packages(),
    install_requires=[
        "openai>=1.37.0",
        "colorama>=04.6"
    ],
    entry_points={
        'console_scripts': [
            'ai-commit=git_diff:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

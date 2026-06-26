import os
from setuptools import setup, find_packages

setup(
    name="puralang",
    version="1.0.0",
    author="Sai Darsini",
    description="An AI-driven domain-specific language engine for automated data cleaning pipelines.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/puralang_engine",
    packages=find_packages(),
    install_requires=[
        "lark",
        "rich",
        "pandas",
        "typer",
        "google-genai"
    ],
    entry_points={
        "console_scripts": [
            "pura=puralang.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
import os
from setuptools import setup, find_packages

# Safely read the README file using UTF-8 encoding to avoid Windows charmap errors
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = ""

setup(
    name="puralang-engine",
    version="1.0.4",
    author="Sai Darsini Sathuluru",
    author_email="saidarsini05@gmail.com",
    description="An AI-driven domain-specific language engine for automated data cleaning pipelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaiDarsini/puralang_engine",
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
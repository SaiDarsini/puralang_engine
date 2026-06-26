# PuraLang Engine 🚀

> **An AI-powered Domain-Specific Language for automated data cleaning pipelines.**  
> Describe your data problem in plain English — PuraLang writes and runs the pipeline for you.

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.8+-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  <a href="https://puralangengine-zwuemzwdpalt53atsjjmnp.streamlit.app/">
    <img src="https://img.shields.io/badge/🌐 Live Demo-Try PuraLang Now-FF4B4B?style=for-the-badge" />
  </a>
</p>

---

## What is PuraLang?

PuraLang is a custom programming language built specifically for **data cleaning**. Instead of writing 30–50 lines of Python/Pandas code every time you need to clean a dataset, you write a clean, human-readable `.pura` script — or better yet, just **describe what you want in English** and let the AI generate the script for you.

### The Problem It Solves

Every data engineer and ML practitioner spends hours writing repetitive boilerplate code like this:

```python
import pandas as pd
df = pd.read_csv("users.csv")
df = df.drop_duplicates(subset=["user_id"])
df["age"] = df["age"].fillna(24)
df["email"] = df["email"].str.strip().str.lower()
df.to_csv("clean_users.csv", index=False)
```

With PuraLang, the same result is achieved in 5 readable lines:

```
LOAD "users.csv"
  |> DROP_DUPLICATES "user_id"
  |> FILL_NULLS "age" VALUE 24
  |> FORMAT_STRINGS "email" TO LOWERCASE
  |> EXPORT_CSV "clean_users.csv"
```

And with **AI Mode**, you don't even need to write that:

```bash
puralang ask "clean users.csv — remove duplicate user IDs, fill missing ages with 24, lowercase all emails"
```

---

## Features

- **Custom DSL Syntax** — Clean, readable pipeline syntax with `|>` operators
- **AI Mode** — Describe your cleaning task in plain English; the engine generates and runs the script automatically
- **Visual Execution Trace** — Beautiful terminal output showing row counts before and after every operation
- **Multiple Operations** — DROP_DUPLICATES, FILL_NULLS, FORMAT_STRINGS, FILTER_ROWS, EXPORT_CSV
- **Zero Boilerplate** — No Pandas knowledge required to use it

---

## Installation

```bash
pip install puralang-engine
```

Or clone and run locally:

```bash
git clone https://github.com/SaiDarsini/puralang_engine.git
cd puralang_engine
pip install -r requirements.txt
```

---

## Quick Start

### Manual Mode — Write a `.pura` script

Create a file called `pipeline.pura`:

```
LOAD "dirty_data.csv"
  |> DROP_DUPLICATES "user_id"
  |> FILL_NULLS "age" VALUE 24
  |> FORMAT_STRINGS "email" TO LOWERCASE
  |> EXPORT_CSV "cleaned_output.csv"
```

Run it:

```bash
puralang run pipeline.pura
```

### AI Mode — Describe it in English

```bash
puralang ask "load sales.csv, remove duplicate order IDs, fill missing prices with 0, export to clean_sales.csv"
```

PuraLang will:
1. Send your description to an AI model
2. Show you the generated `.pura` script
3. Execute it automatically
4. Print the trace report

---

## Execution Output

Every pipeline run produces a visual trace table in your terminal:

```
 ┌─────────────────────────── PuraLang Execution Trace ───────────────────────────┐
 │ Operation                      │ Rows Before │ Rows After │
 ├────────────────────────────────┼─────────────┼────────────┤
 │ LOAD SOURCE DATA               │ -           │ 4          │
 │ DROP DUPLICATES [user_id]      │ 4           │ 3          │
 │ FILL NULL FIELDS [age]         │ 3           │ 3          │
 │ STRING TRANSFORM [email]       │ 3           │ 3          │
 │ EXPORT COMPILED FILE           │ 3           │ 3          │
 └────────────────────────────────┴─────────────┴────────────┘
```

---

## Supported Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Load CSV | `LOAD "file.csv"` | Load a CSV file into the pipeline |
| Drop Duplicates | `DROP_DUPLICATES "column"` | Remove duplicate rows based on a column |
| Fill Nulls | `FILL_NULLS "column" VALUE 0` | Fill missing values with a default |
| Format Strings | `FORMAT_STRINGS "column" TO LOWERCASE` | Normalize text casing |
| Filter Rows | `FILTER_ROWS "column" GREATER_THAN 18` | Filter rows by condition |
| Export CSV | `EXPORT_CSV "output.csv"` | Save cleaned data to a new file |

---

## Project Architecture

```
puralang_engine/
│
├── puralang/
│   ├── __init__.py       # Package version
│   ├── core.py           # Lark grammar, parser, and transformer engine
│   └── cli.py            # Typer CLI — run and ask commands
│
├── tests/
│   └── sample.pura       # Example PuraLang script
│
├── setup.py              # PyPI packaging config
└── README.md
```

The engine works in 3 stages:

```
.pura script → [Lark Parser] → Abstract Syntax Tree → [Transformer] → Pandas execution → Clean CSV
```

For AI Mode:

```
English prompt → [LLM API] → .pura script → [Engine] → Clean CSV
```

---

## Tech Stack

- **Lark** — Grammar definition and parsing
- **Pandas** — Underlying data manipulation engine
- **Rich** — Beautiful terminal output and trace tables
- **Typer** — CLI command interface
- **Google Gemini API** — AI script generation (AI Mode)

---

## Roadmap

- [x] Core DSL parser and transformer
- [x] CLI with `run` command
- [x] AI Mode with `ask` command
- [x] Visual execution trace table
- [x] Live Web UI (Streamlit)
- [ ] PyPI public release (`pip install puralang-engine`)
- [ ] Support for JSON and Excel input formats
- [ ] VS Code extension with `.pura` syntax highlighting

---

## About the Author

**Sai Darsini Sathuluru**  
B.Tech Student | Mohan Babu University | Generative AI Intern @ Prodigy InfoTech  
Founder & Core Architect of PuraLang Engine

- GitHub: [@SaiDarsini](https://github.com/SaiDarsini)
- LinkedIn: [Connect here](https://www.linkedin.com/in/sai-darsini-s-893967322/)

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it.  
See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by Sai Darsini · If this helped you, please ⭐ the repo!
</p>

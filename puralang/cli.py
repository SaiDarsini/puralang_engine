import typer
from puralang.core import run_pure_script, ask_ai_to_clean

app = typer.Typer(help="PuraLang CLI Framework")

@app.command()
def run(script_path: str = typer.Argument(..., help="Path targeting your local .pura script file.")):
    """Runs a local manual PuraLang script file."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        run_pure_script(content)
    except Exception as e:
        typer.secho(f"Compiler Error: {e}", fg=typer.colors.RED, bold=True)

@app.command()
def ask(prompt: str = typer.Argument(..., help="Describe your data cleaning goals in plain English.")):
    """AI Mode: Describe your data cleaning goals in plain English."""
    try:
        ask_ai_to_clean(prompt)
    except Exception as e:
        typer.secho(f"AI Pipeline Execution Failure: {e}", fg=typer.colors.RED, bold=True)

if __name__ == "__main__":
    app()
import os
import sys
import pandas as pd
from lark import Lark, Transformer
from google import genai
from google.genai import types
from rich.console import Console
from rich.table import Table

puralang_grammar = """
    start: pipeline
    pipeline: load_stmt (pipe step_stmt)*
    
    load_stmt: "LOAD" ESCAPED_STRING
    step_stmt: drop_dup | fill_null | format_str | filter_rows | rename_col | export_csv
    
    drop_dup: "DROP_DUPLICATES" ESCAPED_STRING
    fill_null: "FILL_NULLS" ESCAPED_STRING "VALUE" (ESCAPED_STRING | NUMBER)
    format_str: "FORMAT_STRINGS" ESCAPED_STRING "TO" CASE_ACTION
    filter_rows: "FILTER_ROWS" ESCAPED_STRING OPERATOR NUMBER
    rename_col: "RENAME_COLUMN" ESCAPED_STRING "TO" ESCAPED_STRING
    export_csv: "EXPORT_CSV" ESCAPED_STRING
    
    pipe: "|>"
    CASE_ACTION: "LOWERCASE" | "UPPERCASE"
    OPERATOR: ">" | "<" | "==" | "!="
    
    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

class PuraTransformer(Transformer):
    def __init__(self):
        self.df = None
        self.console = Console()
        self.report = Table(title="PuraLang Execution Trace", show_header=True, header_style="bold cyan")
        self.report.add_column("Pipeline Step", style="magenta")
        self.report.add_column("Rows Before", style="yellow")
        self.report.add_column("Rows After", style="green")

    def load_stmt(self, items):
        filename = items[0].strip('"')
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Missing input dataset file: '{filename}'")
        self.df = pd.read_csv(filename)
        self.report.add_row("LOAD SOURCE DATA", "-", str(len(self.df)))
        return self.df

    def drop_dup(self, items):
        col = items[0].strip('"')
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=[col])
        self.report.add_row(f"DROP DUPLICATES [{col}]", str(before), str(len(self.df)))

    def fill_null(self, items):
        col = items[0].strip('"')
        raw_val = items[1]
        val = raw_val.strip('"') if hasattr(raw_val, 'type') and raw_val.type == "ESCAPED_STRING" else float(raw_val)
        before = len(self.df)
        self.df[col] = self.df[col].fillna(val)
        self.report.add_row(f"FILL NULL FIELDS [{col}]", str(before), str(len(self.df)))

    def format_str(self, items):
        col = items[0].strip('"')
        case_type = str(items[1]).strip()
        before = len(self.df)
        if "LOWERCASE" in case_type:
            self.df[col] = self.df[col].astype(str).str.strip().str.lower()
        else:
            self.df[col] = self.df[col].astype(str).str.strip().str.upper()
        self.report.add_row(f"STRING TRANSFORM [{col} -> {case_type}]", str(before), str(len(self.df)))

    def filter_rows(self, items):
        col = items[0].strip('"')
        op = str(items[1]).strip()
        val = float(items[2])
        before = len(self.df)
        
        # Dynamic pandas evaluation bypass
        if op == ">": self.df = self.df[self.df[col] > val]
        elif op == "<": self.df = self.df[self.df[col] < val]
        elif op == "==": self.df = self.df[self.df[col] == val]
        elif op == "!=": self.df = self.df[self.df[col] != val]
        
        self.report.add_row(f"FILTER ROWS [{col} {op} {val}]", str(before), str(len(self.df)))

    def rename_col(self, items):
        old_col = items[0].strip('"')
        new_col = items[1].strip('"')
        before = len(self.df)
        self.df = self.df.rename(columns={old_col: new_col})
        self.report.add_row(f"RENAME COLUMN [{old_col} -> {new_col}]", str(before), str(len(self.df)))

    def export_csv(self, items):
        filename = items[0].strip('"')
        self.df.to_csv(filename, index=False)
        self.report.add_row(f"EXPORT COMPILED FILE", str(len(self.df)), str(len(self.df)))

    def pipeline(self, items):
        self.console.print(self.report)
        return self.df

def run_pure_script(script_content: str):
    parser = Lark(puralang_grammar, start='start')
    tree = parser.parse(script_content)
    transformer = PuraTransformer()
    transformer.transform(tree)

def ask_ai_to_clean(user_prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    system_instruction = """
    You are the natural language translation engine for PuraLang, a data-cleaning DSL.
    Your sole job is to translate a user's plain English cleaning request into a valid PuraLang script.
    
    VALID KEYWORDS AND SYNTAX:
    LOAD "filename.csv"
      |> DROP_DUPLICATES "column_name"
      |> FILL_NULLS "column_name" VALUE 20
      |> FORMAT_STRINGS "column_name" TO LOWERCASE
      |> FILTER_ROWS "column_name" > 50
      |> RENAME_COLUMN "old_name" TO "new_name"
      |> EXPORT_CSV "output.csv"
      
    CRITICAL INSTRUCTIONS:
    - Respond ONLY with the raw PuraLang code script. 
    - Do NOT include markdown code blocks like ```text or ```puralang.
    - Do NOT write any conversational filler text.
    """

    print("🤖 Consulting PuraLang AI Agent...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Translate this cleaning request into PuraLang code:\n\n{user_prompt}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )
    
    generated_code = response.text.strip()
    
    console = Console()
    console.print("\n[bold green]✨ AI Generated PuraLang Script Layout:[/bold green]")
    console.print(f"[dim]{generated_code}[/dim]\n")
    
    run_pure_script(generated_code)
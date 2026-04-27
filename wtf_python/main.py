import typer
import os
import re
import shutil
from typing import Optional
from rich.prompt import Confirm
from wtf_python.executor import run_python_script
from wtf_python.ai import explain_error
from wtf_python.formatter import show_divider, display_explanation, get_console

app = typer.Typer()
console = get_console()

def extract_code(text: str) -> str:
    """
    Extracts the first python code block from a markdown string.
    Handles ```python, ```py, or just ``` code blocks.
    """
    # Try to find python specific blocks first
    pattern = r"```(?:python|py)\s+(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Fallback to any code block if no python block is found
    fallback_pattern = r"```\s+(.*?)```"
    match = re.search(fallback_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    return ""

@app.command()
def main(
    script_path: str,
    socrates: bool = typer.Option(False, "--socrates", help="Wise mentor persona"),
    dummy: bool = typer.Option(False, "--dummy", help="Kindergarten analogies persona"),
    roast: bool = typer.Option(False, "--roast", help="Gordon Ramsay roast persona"),
    bro: bool = typer.Option(False, "--bro", help="Silicon Valley bro persona"),
    wizard: bool = typer.Option(False, "--wizard", help="Medieval sorcerer persona")
):
    """
    Runs a Python script and intercepts errors with AI-powered explanations and auto-fixes.
    """
    if not os.path.exists(script_path):
        console.print(f"[bold red]Error:[/bold red] File '{script_path}' not found.")
        raise typer.Exit(code=1)

    # Determine personality
    personality = None
    if socrates: personality = "socrates"
    elif dummy: personality = "dummy"
    elif roast: personality = "roast"
    elif bro: personality = "bro"
    elif wizard: personality = "wizard"

    stdout, stderr, returncode = run_python_script(script_path)
    
    if returncode != 0:
        show_divider()
        
        # Read the broken script code
        try:
            with open(script_path, "r") as f:
                code = f.read()
        except Exception as e:
            code = f"Could not read file: {e}"

        try:
            with console.status("[bold green]Asking the Python Gods what happened...[/bold green]", spinner="bouncingBar") as status:
                explanation = explain_error(code, stderr, status=status, personality=personality)
            
            display_explanation(explanation)
            
            # Phase 3 & 4: Auto-Fixer with Backup
            corrected_code = extract_code(explanation)
            if corrected_code:
                if Confirm.ask("[bold cyan]Would you like me to apply this fix to your file?[/bold cyan]"):
                    try:
                        # Create backup
                        backup_path = f"{script_path}.bak"
                        shutil.copy2(script_path, backup_path)
                        
                        # Apply fix
                        with open(script_path, "w") as f:
                            f.write(corrected_code)
                        
                        # Verify
                        with open(script_path, "r") as f:
                            new_content = f.read()
                        
                        if new_content == corrected_code:
                            console.print(f"[bold green]✔ Fix applied![/bold green] [dim](Original file backed up to {backup_path})[/dim]")
                        else:
                            console.print("[bold red]ERROR: Verification failed.[/bold red]")
                    except Exception as write_err:
                        console.print(f"[bold red]Write failed:[/bold red] {write_err}")
            else:
                console.print("[yellow]Could not extract a code fix from the AI response.[/yellow]")

        except Exception as e:
            console.print(f"[bold red]Error connecting to AI:[/bold red] {e}")
            # Fallback to printing stderr if AI fails
            console.print(stderr)
    else:
        # If success, print the stdout as usual
        if stdout:
            print(stdout, end="")

if __name__ == "__main__":
    app()

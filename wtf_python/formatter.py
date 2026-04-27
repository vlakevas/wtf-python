from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.rule import Rule

console = Console()

def show_divider():
    """Prints a bold red divider."""
    console.print(Rule(style="bold red"))

def get_console():
    return console

def display_explanation(markdown_text: str):
    """Renders the Gemini response in a beautiful panel."""
    md = Markdown(markdown_text)
    panel = Panel(
        md,
        title="[bold red]Oops! Let's fix this.[/bold red]",
        border_style="cyan",
        expand=False
    )
    console.print(panel)

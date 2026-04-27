import os
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

def explain_error(code: str, traceback: str, status=None, personality: str = None) -> str:
    """
    Sends the code and traceback to Gemini and returns a friendly explanation.
    Includes exponential backoff for rate limits (429) and AI personalities.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console = Console()
        console.print("[bold red]Error: GEMINI_API_KEY not found in environment.[/bold red]")
        console.print("Please set your API key in a [bold].env[/bold] file or as an environment variable.")
        console.print("Example: [cyan]GEMINI_API_KEY=your_key_here[/cyan]")
        raise ValueError("Missing GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    # Base instructions
    system_prompt = (
        "You are 'wtf-python', a friendly AI assistant that helps beginner programmers understand Python errors. "
        "Your goal is to translate confusing tracebacks into jargon-free, actionable advice. "
        "\n\nCRITICAL: While the traceback highlights one specific error, you MUST scan the entire code snippet "
        "for any other obvious bugs, logical errors, or potential crashes (like missing imports, undefined variables, "
        "or type mismatches) and fix them all in your provided solution."
        "\n\nStrictly follow this three-part format in your response:\n\n"
        "### What Happened\n"
        "(A simple explanation according to your persona)\n\n"
        "### Where It Happened\n"
        "(Identify the lines of code and explain what they were trying to do)\n\n"
        "### How to Fix It\n"
        "(Step-by-step instructions. You MUST provide the COMPLETE, corrected file content inside "
        "a standard markdown Python code block (```python ... ```) that resolves ALL identified issues.)"
    )

    # Personality dynamic instructions
    personas = {
        "socrates": "\n\nPERSONALITY: Act as a wise mentor. Do NOT just give the answer immediately in your explanation. Explain the concept deeply and ask a guiding question to help the user spot the error themselves. However, ALWAYS include the corrected code block at the end.",
        "dummy": "\n\nPERSONALITY: Act like Mister Rogers teaching kindergarten. Assume zero technical background. Replace all programming jargon with real-world physical analogies like boxes, recipes, or physical objects.",
        "roast": "\n\nPERSONALITY: Act like Gordon Ramsay reviewing code. Be harsh, sarcastic, and deeply disappointed in the user. Use insults related to their lack of skill, but still provide the correct fix. Your explanation should be a 'roast'.",
        "bro": "\n\nPERSONALITY: Act like a hyper-caffeinated Silicon Valley 10x startup founder. Use excessive startup jargon like 'pivoting', 'MVP', 'alignment', 'synergy', and 'disruption'. Everything is about scale and paradigms.",
        "wizard": "\n\nPERSONALITY: Act as a medieval sorcerer. Treat bugs as dark magic, curses, or demonic possessions. Treat the fix as a counter-spell or a holy ritual. Use archaic, mystical language."
    }

    if personality and personality in personas:
        system_prompt += personas[personality]

    prompt = (
        f"{system_prompt}\n\n"
        f"The user's code:\n```python\n{code}\n```\n\n"
        f"The error message (traceback):\n```text\n{traceback}\n```"
    )

    retries = 0
    max_retries = 3
    backoff_times = [10, 20, 30]

    while retries <= max_retries:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except errors.APIError as e:
            if e.status_code == 429 and retries < max_retries:
                sleep_time = backoff_times[retries]
                if status:
                    status.update(f"[bold yellow]Rate limit hit (5 RPM max). Waiting {sleep_time}s to retry...[/bold yellow]")
                time.sleep(sleep_time)
                retries += 1
                if status:
                    status.update("[bold green]Asking the Python Gods what happened...[/bold green]")
            else:
                if e.status_code == 429:
                    raise Exception("API quota exceeded (5 RPM). Please wait a minute before trying again.")
                raise e
        except Exception as e:
            raise e

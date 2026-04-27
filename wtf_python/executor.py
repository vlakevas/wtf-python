import subprocess
import sys

def run_python_script(script_path: str):
    """Runs a python script and captures its output and error."""
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

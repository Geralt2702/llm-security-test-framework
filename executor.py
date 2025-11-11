import subprocess
import time

def query_model(model, prompt, timeout=60):
    try:
        result = subprocess.run(
            ["ollama", "run", model, "--cpu", "--prompt", prompt],
            capture_output=True, text=True, timeout=timeout)
        if result.stderr:
            print(f"Error output: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

import subprocess
from ..executor import get_temp_path

def _run_go(code: str):
    temp_go = get_temp_path("temp.go")
    
    with open(temp_go, "w") as f:
        f.write(code)
    
    result = subprocess.run(["go", "run", temp_go], capture_output=True, text=True)
    
    return result.stdout


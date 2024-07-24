import subprocess
from ..executor import get_temp_path

def _run_javascript(code: str):
    temp_js = get_temp_path("temp.js")
    
    with open(temp_js, "w") as f:
        f.write(code)
    
    result = subprocess.run(["node", temp_js], capture_output=True, text=True)
    
    return result.stdout


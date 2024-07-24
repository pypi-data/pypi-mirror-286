import subprocess
from ..executor import get_temp_path

def _run_swift(code: str):
    temp_swift = get_temp_path("temp.swift")
    
    with open(temp_swift, "w") as f:
        f.write(code)
    
    result = subprocess.run(["swift", temp_swift], capture_output=True, text=True)
    
    return result.stdout


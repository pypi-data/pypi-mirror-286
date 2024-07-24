import subprocess
from ..executor import get_temp_path

def _run_haskell(code: str):
    temp_hs = get_temp_path("script.hs")
    temp_executable = get_temp_path("script")
    
    with open(temp_hs, "w") as f:
        f.write(code)
    
    subprocess.run(["ghc", "-o", temp_executable, temp_hs], check=True)
    result = subprocess.run([temp_executable], capture_output=True, text=True)
    
    return result.stdout


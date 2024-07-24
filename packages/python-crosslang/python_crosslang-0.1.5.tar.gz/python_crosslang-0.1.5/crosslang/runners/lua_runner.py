import subprocess
from ..executor import get_temp_path

def _run_lua(code: str):
    temp_lua = get_temp_path("temp.lua")

    with open(temp_lua, "w") as f:
        f.write(code)
    
    result = subprocess.run(["lua", temp_lua], capture_output=True, text=True)
    
    return result.stdout

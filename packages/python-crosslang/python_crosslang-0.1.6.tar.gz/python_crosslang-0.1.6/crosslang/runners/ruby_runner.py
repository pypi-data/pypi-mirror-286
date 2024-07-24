import subprocess
from ..executor import get_temp_path

def _run_ruby(code: str):
    temp_rb = get_temp_path("temp.rb")

    with open(temp_rb, "w") as f:
        f.write(code)
    
    result = subprocess.run(["ruby", temp_rb], capture_output=True, text=True)
    
    return result.stdout

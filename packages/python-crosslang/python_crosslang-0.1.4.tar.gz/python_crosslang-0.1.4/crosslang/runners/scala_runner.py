import subprocess
from ..executor import get_temp_path

def _run_scala(code: str):
    temp_scala = get_temp_path("temp.scala")
    
    with open(temp_scala, "w") as f:
        f.write(code)
    
    result = subprocess.run(["scala", temp_scala], capture_output=True, text=True)
    
    return result.stdout


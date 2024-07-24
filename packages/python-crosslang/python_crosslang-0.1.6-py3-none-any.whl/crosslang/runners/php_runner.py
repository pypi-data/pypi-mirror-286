import subprocess
from ..executor import get_temp_path

def _run_php(code: str):
    temp_php = get_temp_path("temp.php")
    
    with open(temp_php, "w") as f:
        f.write(code)
    
    result = subprocess.run(["php", temp_php], capture_output=True, text=True)
    
    return result.stdout


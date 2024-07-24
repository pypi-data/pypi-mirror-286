import subprocess
from ..executor import get_temp_path

def _run_perl(code: str):
    temp_pl = get_temp_path("temp.pl")
    
    with open(temp_pl, "w") as f:
        f.write(code)
    
    result = subprocess.run(["perl", temp_pl], capture_output=True, text=True)
    
    return result.stdout


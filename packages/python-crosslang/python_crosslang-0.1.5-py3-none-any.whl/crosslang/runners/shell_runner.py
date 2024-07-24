import subprocess
from ..executor import get_temp_path

def _run_shell(code: str):
    temp_sh = get_temp_path("temp.sh")
    
    with open(temp_sh, "w") as f:
        f.write(code)
    
    subprocess.run(["chmod", "+x", temp_sh])
    result = subprocess.run(["bash", temp_sh], capture_output=True, text=True)
    
    return result.stdout


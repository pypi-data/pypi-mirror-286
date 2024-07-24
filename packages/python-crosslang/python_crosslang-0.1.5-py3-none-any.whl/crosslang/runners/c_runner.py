import subprocess
from  ..executor import get_temp_path

def _run_c(code: str):
    temp_c = get_temp_path("temp.c")
    temp_executable = get_temp_path("temp_executable")

    with open(temp_c, "w") as f:
        f.write(code)
    
    subprocess.run(["gcc", temp_c, "-o", temp_executable], check=True)
    result = subprocess.run([temp_executable], capture_output=True, text=True)
    
    return result.stdout

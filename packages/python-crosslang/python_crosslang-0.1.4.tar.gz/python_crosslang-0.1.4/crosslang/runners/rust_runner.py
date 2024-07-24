import subprocess
from ..executor import get_temp_path

def _run_rust(code: str):
    temp_rs = get_temp_path("temp.rs")
    temp_executable = get_temp_path("temp_executable")

    with open(temp_rs, "w") as f:
        f.write(code)
    
    subprocess.run(["rustc", temp_rs, "-o", temp_executable], check=True)
    result = subprocess.run([temp_executable], capture_output=True, text=True)
    
    return result.stdout

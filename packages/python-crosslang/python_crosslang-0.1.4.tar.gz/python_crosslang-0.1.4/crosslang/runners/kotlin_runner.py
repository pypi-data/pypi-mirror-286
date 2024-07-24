import subprocess
from ..executor import get_temp_path

def _run_kotlin(code: str):
    temp_kt = get_temp_path("script.kt")
    temp_jar = get_temp_path("script.jar")
    
    with open(temp_kt, "w") as f:
        f.write(code)
    
    subprocess.run(["kotlinc", temp_kt, "-include-runtime", "-d", temp_jar], check=True)
    result = subprocess.run(["kotlin", temp_jar], capture_output=True, text=True)
    
    return result.stdout



import subprocess
import re
import os
from pathlib import Path

def _run_java(code: str) -> str:
    # Create a temp directory for Java files
    temp_dir = Path(__file__).parent / 'temp_files'
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract class name
    class_name_match = re.search(r'public\s+class\s+(\w+)', code)
    if not class_name_match:
        raise ValueError("No public class found in Java code.")
    class_name = class_name_match.group(1)
    temp_java = temp_dir / f"{class_name}.java"
    temp_class = temp_dir / class_name

    # Write the Java code to a file
    with open(temp_java, 'w') as file:
        file.write(code)
    
    # Compile the Java code
    try:
        subprocess.run(["javac", str(temp_java)], check=True)
    except subprocess.CalledProcessError as e:
        return f"Compilation Error:\n{e}"
    
    # Run the Java code
    try:
        result = subprocess.run(["java", "-cp", str(temp_dir), class_name], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Runtime Error:\n{e}\n{e.stderr}"


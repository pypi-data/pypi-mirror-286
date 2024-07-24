
# **Intro**
CrossLang is a Python library that allows developers to run code written in various programming languages directly from their Python scripts. This can be particularly useful for multi-language projects, testing, and automation.

Supports multiple programming languages including Rust, C, Java, Ruby, Lua, Go, JavaScript, PHP, Perl, Scala, Shell, Swift, Kotlin, and Haskell.
Automatically compiles and runs code snippets.
Easy to integrate into existing Python projects.

# **Installation**
To install CrossLang, you can use pip:

```bash
pip install python-crosslang
```
# **Installing Compilers and Interpreters**
CrossLang relies on various external compilers and interpreters to execute code in different languages. You can use the provided installation scripts to set up the necessary dependencies.

For Unix-based Systems (Linux/macOS):
Run the following script to install the required compilers and interpreters:

```bash
chmod +x debian.sh; ./debian.sh
```
For Arch Linux:\
Run the following script to install the required compilers and interpreters:

```bash
chmod +x arch.sh; ./arch.sh
```
For Windows:\
Run the following PowerShell script to install the required compilers and interpreters:

```powershell
.\windows.ps1
```
# **Usage**
Here's an example of how to use CrossLang in your Python script:

```python
from CrossLang import Translator

# Running Rust code
code = """
fn main() {
    println!("Hello, world!");
}
"""

output = Translator('rust', code)
print(output)

# Running C code
code = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""

output = Translator('c', code)
print(output)

# Running Java code
code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

output = Translator('java', code)
print(output)
```

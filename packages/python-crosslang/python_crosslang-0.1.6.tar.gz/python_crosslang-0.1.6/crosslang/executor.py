import os

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp_files')

os.makedirs(TEMP_DIR, exist_ok=True)

def get_temp_path(filename):
    return os.path.join(TEMP_DIR, filename)

def Translator(language: str, code: str, *args, **kwargs):
    try:
        run_function = language_runners[language.lower()]
    except KeyError:
        raise ValueError(f"Unsupported language: {language}")
    
    return run_function(code, *args, **kwargs)

from .runners.rust_runner import _run_rust
from .runners.c_runner import _run_c
from .runners.java_runner import _run_java
from .runners.ruby_runner import _run_ruby
from .runners.lua_runner import _run_lua
from .runners.go_runner import _run_go
from .runners.js_runner import _run_javascript
from .runners.php_runner import _run_php
from .runners.perl_runner import _run_perl
from .runners.scala_runner import _run_scala
from .runners.shell_runner import _run_shell
from .runners.kotlin_runner import _run_kotlin

language_runners = {
    'rust': _run_rust,
    'c': _run_c,
    'java': _run_java,
    'ruby': _run_ruby,
    'lua': _run_lua,
    'go': _run_go,
    'js': _run_javascript,
    'javascript': _run_javascript,
    'php': _run_php,
    'perl': _run_perl,
    'scala': _run_scala,
    'shell': _run_shell,
    'kotlin': _run_kotlin,
}

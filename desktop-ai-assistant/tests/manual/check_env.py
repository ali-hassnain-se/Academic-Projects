"""Checks that every required package imports. Run on Windows."""
import importlib
import sys

PACKAGES = {
    "PySide6": "PySide6",
    "platformdirs": "platformdirs",
    "markdown": "markdown",
    "pygments": "Pygments",
    "google.genai": "google-genai",
    "keyring": "keyring",
    "ollama": "ollama",
    "pynput": "pynput",
    "pyperclip": "pyperclip",
    "mss": "mss",
    "PIL": "Pillow",
    "psutil": "psutil",
    "win32gui": "pywin32",
    "pytest": "pytest",
    "PyInstaller": "pyinstaller",
}

print("Python:", sys.version.split()[0])
failed = []
for module, pip_name in PACKAGES.items():
    try:
        importlib.import_module(module)
        print(f"  OK    {pip_name}")
    except Exception as e:
        print(f"  FAIL  {pip_name}  ({type(e).__name__}: {e})")
        failed.append(pip_name)

print()
print("All good!" if not failed else f"Missing/broken: {', '.join(failed)}")
sys.exit(1 if failed else 0)

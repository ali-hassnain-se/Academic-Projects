"""Start with Windows. Owner: Member C.

Adds / removes one value in the current user's Run registry key:
    HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
HKCU needs no administrator rights and only affects the current Windows user.

'winreg' exists only on Windows, so it is imported inside the functions
(this keeps the file importable on Linux/WSL for tests)."""
import sys
from pathlib import Path

_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_NAME = "DesktopAIAssistant"


def _command() -> str:
    """The command Windows will run at login.

    - Packaged app (.exe built by PyInstaller): run the .exe itself.
    - Running from source: run main.py with pythonw.exe (no black console window).
      The path is built from this file's location, NOT from the current folder,
      because at login Windows starts programs in a different working folder."""
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'

    python = Path(sys.executable)
    pythonw = python.with_name("pythonw.exe")
    interpreter = pythonw if pythonw.exists() else python
    main_py = Path(__file__).resolve().parents[2] / "main.py"
    return f'"{interpreter}" "{main_py}"'


def enable_autostart() -> None:
    """Start the assistant automatically when the user logs in to Windows.
    Raises OSError if the registry cannot be written (the GUI should show it)."""
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, _NAME, 0, winreg.REG_SZ, _command())


def disable_autostart() -> None:
    """Remove the auto-start entry (does nothing if it does not exist)."""
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY, 0, winreg.KEY_SET_VALUE) as key:
        try:
            winreg.DeleteValue(key, _NAME)
        except FileNotFoundError:
            pass


def is_autostart_enabled() -> bool:
    """True if the auto-start entry exists."""
    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY) as key:
            winreg.QueryValueEx(key, _NAME)
            return True
    except FileNotFoundError:
        return False
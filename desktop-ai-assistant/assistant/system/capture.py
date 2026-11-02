"""Selected text, screenshot, active app. Owner: Member C.

All heavy / Windows-only imports are done inside the functions, so this file
can be imported (and tested) on Linux/WSL too."""
import io
import time


# ---------------------------------------------------------------
# 1. Selected text
# ---------------------------------------------------------------
def get_selected_text() -> str:
    """Return the text currently selected in any app ('' if nothing is selected).

    Trick: put a marker on the clipboard, simulate Ctrl+C, and see if it changed.
    The user's original clipboard is always restored."""
    import pyperclip
    from pynput.keyboard import Controller, Key

    kb = Controller()
    try:
        original = pyperclip.paste()
    except Exception:
        original = ""

    marker = f"__DAI_MARKER_{time.time_ns()}__"
    text = marker
    try:
        pyperclip.copy(marker)
        # Hotkey keys may still be held down; release them so we send a clean Ctrl+C
        for k in (Key.shift, Key.alt):
            kb.release(k)
        time.sleep(0.15)
        with kb.pressed(Key.ctrl):
            kb.press("c")
            kb.release("c")
        time.sleep(0.2)
        text = pyperclip.paste()
    except Exception:
        text = marker
    finally:
        try:
            pyperclip.copy(original)
        except Exception:
            pass

    return "" if text == marker else text.strip()


# ---------------------------------------------------------------
# 2. Active application
# ---------------------------------------------------------------
def classify_app(process_name: str) -> str:
    """Map a Windows process name to 'vscode' | 'browser' | 'other'."""
    name = process_name.lower()
    if name in {"code.exe", "code - insiders.exe", "cursor.exe"}:
        return "vscode"
    if name in {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"}:
        return "browser"
    return "other"


def _active_process_name() -> str:
    """Process name of the window that currently has focus (e.g. 'chrome.exe')."""
    import psutil
    import win32gui
    import win32process

    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return psutil.Process(pid).name()


def get_active_app() -> str:
    """Returns 'vscode', 'browser' or 'other'. Never raises.

    NOTE: call this BEFORE showing the assistant window, otherwise our own
    window has the focus and the answer will always be 'other'."""
    try:
        return classify_app(_active_process_name())
    except Exception:
        return "other"


# ---------------------------------------------------------------
# 3. Screenshot
# ---------------------------------------------------------------
def take_screenshot(max_width: int = 1600) -> bytes:
    """Screenshot of the primary monitor as PNG bytes.

    The image is shrunk to max_width so the AI request stays small and fast.
    NOTE: the GUI must hide its own window before calling this."""
    import mss
    from PIL import Image

    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[1])          # monitors[0] = all screens, [1] = primary
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")

    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
"""Selected text, screenshot, active app. Owner: Member C.

All heavy / Windows-only imports are done inside the functions, so this file
can be imported (and tested) on Linux/WSL too."""
import io
import time


# ---------------------------------------------------------------
# 1. Selected text
# ---------------------------------------------------------------
def _wait_for_keys_released(timeout: float = 1.0) -> None:
    """Wait until Shift / Ctrl / Alt / Space are physically released.

    The hotkey fires while the user is still holding its keys. Sending Ctrl+C
    at that moment often fails, so we wait for the user to let go first."""
    try:
        import ctypes

        user32 = ctypes.windll.user32
    except Exception:
        time.sleep(0.2)
        return

    keys = (0x10, 0x11, 0x12, 0x20)         # Shift, Ctrl, Alt, Space
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not any(user32.GetAsyncKeyState(vk) & 0x8000 for vk in keys):
            return
        time.sleep(0.02)


def get_selected_text() -> str:
    """Return the text currently selected in any app ('' if nothing is selected).

    Trick: put a marker on the clipboard, simulate Ctrl+C, and see if it changed.
    The user's original clipboard text is restored afterwards."""
    import pyperclip
    from pynput.keyboard import Controller, Key

    kb = Controller()
    try:
        original = pyperclip.paste()
    except Exception:
        original = ""

    result = ""
    try:
        _wait_for_keys_released()
        for k in (Key.shift, Key.alt):      # in case a key is still logically down
            kb.release(k)

        for _attempt in range(2):
            marker = f"__DAI_MARKER_{time.time_ns()}__"
            pyperclip.copy(marker)
            time.sleep(0.05)

            with kb.pressed(Key.ctrl):
                kb.press("c")
                kb.release("c")

            # Wait up to ~0.6 s for the app to put the selection on the clipboard.
            text = marker
            deadline = time.time() + 0.6
            while time.time() < deadline:
                time.sleep(0.05)
                text = pyperclip.paste()
                if text != marker:
                    break

            if text != marker:
                result = text.strip()
                break
    except Exception:
        result = ""
    finally:
        try:
            pyperclip.copy(original)
        except Exception:
            pass

    return result


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
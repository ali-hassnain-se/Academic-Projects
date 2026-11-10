"""Entry point of the Desktop AI Assistant.

Wires everything together:
  hotkey (system)  ->  capture selected text + active app (system)
                   ->  chat window (ui)  ->  AI client (ai)
"""
import json
import sys

from PySide6.QtCore import QDir, QLockFile, QObject, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from assistant import config
from assistant.paths import resource_path, settings_file
from assistant.system.capture import get_active_app, get_selected_text, take_screenshot
from assistant.system.hotkey_manager import HotkeyManager
from assistant.ui.bubble import Bubble
from assistant.ui.chat_window import ChatWindow
from assistant.ui.tray import SystemTray

try:
    from assistant.ai.prompts import pick_mode
except ImportError:                                   # fallback if the helper does not exist
    def pick_mode(app_name: str) -> str:
        return {"vscode": "coding", "browser": "lecture"}.get(app_name, "general")

MAX_SELECTED_CHARS = 4000


def load_hotkey() -> str:
    """Hotkey saved in Settings ('Ctrl + Shift + Space' -> 'ctrl+shift+space')."""
    try:
        data = json.loads(settings_file().read_text(encoding="utf-8"))
        text = data.get("hotkey")
        if text:
            return text.lower().replace(" ", "")
    except Exception:
        pass
    return config.DEFAULT_HOTKEY


class Controller(QObject):
    """Connects the hotkey, the bubble and the chat window."""

    def __init__(self, bubble, chat, hotkeys):
        super().__init__()
        self.bubble = bubble
        self.chat = chat
        self.hotkeys = hotkeys

        bubble.double_clicked.connect(self.show_chat)
        chat.screen_requested.connect(self.explain_screen)
        hotkeys.triggered.connect(self.on_hotkey)

    def show_chat(self):
        self.chat.show()
        self.chat.raise_()
        self.chat.activateWindow()
        self.chat.input_field.setFocus()

    def on_hotkey(self):
        """Runs on the main thread (the hotkey thread only sends a signal)."""
        if self.chat.isVisible() and self.chat.isActiveWindow():
            self.chat.hide()
            return

        # Capture BEFORE our window opens, otherwise our window has the focus.
        app_name = get_active_app()
        selected = get_selected_text()

        print("DEBUG app:", app_name, "| selected chars:", len(selected))

        self.chat.context_mode = pick_mode(app_name)
        self.show_chat()

        if selected:
            selected = selected[:MAX_SELECTED_CHARS]
            text = f"Explain this:\n{selected}"
            self.chat.submit(text, self.chat.context_mode)

    def explain_screen(self):
        # Hide our own windows first so they are not in the screenshot.
        self.chat.hide()
        self.bubble.hide()
        QTimer.singleShot(300, self._capture_and_ask)

    def _capture_and_ask(self):
        png = None
        error = ""
        try:
            png = take_screenshot()
        except Exception as exc:
            error = str(exc)

        self.bubble.show()
        self.show_chat()

        if png:
            self.chat.submit(
                "Explain what is on my screen.",
                "screen",
                image=png,
            )
        else:
            self.chat.add_message(f"Could not take a screenshot: {error}", is_user=False)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setQuitOnLastWindowClosed(False)          # keep running in the tray

    # Only one copy of the assistant at a time (e.g. auto-start + manual start).
    lock = QLockFile(QDir.tempPath() + "/DesktopAIAssistant.lock")
    if not lock.tryLock(100):
        print("Desktop AI Assistant is already running.")
        return 0

    icon = QIcon(resource_path("assets/icon.ico"))
    if not icon.isNull():
        app.setWindowIcon(icon)

    hotkeys = HotkeyManager()
    chat = ChatWindow(hotkeys)
    bubble = Bubble()

    screen = app.primaryScreen().availableGeometry()
    bubble.move(screen.right() - config.BUBBLE_SIZE - 20, screen.top() + 120)
    bubble.show()

    tray = SystemTray(chat, chat.settings_window)
    controller = Controller(bubble, chat, hotkeys)

    if not hotkeys.register(load_hotkey()):
        print("Could not register the hotkey. Use the bubble or the tray icon.")
    app.aboutToQuit.connect(hotkeys.stop)

    code = app.exec()
    lock.unlock()
    # keep references alive until the end
    del tray, controller
    return code


if __name__ == "__main__":
    sys.exit(main())
"""Qt-friendly wrapper around assistant/system/hotkey.py. Owner: Member C.

The hotkey callback runs on a background thread. This class turns it into a Qt
Signal, which Qt delivers safely on the main (GUI) thread."""
from PySide6.QtCore import QObject, Signal

from assistant.system.hotkey import register_hotkey, stop_hotkey


class HotkeyManager(QObject):
    triggered = Signal()

    def __init__(self):
        super().__init__()
        self.current = None

    def register(self, combo: str) -> bool:
        """Start listening for e.g. 'ctrl+space'. Returns False if it fails."""
        try:
            register_hotkey(combo, self.triggered.emit)
            self.current = combo
            return True
        except Exception as error:
            print("Hotkey error:", error)
            return False

    def stop(self) -> None:
        stop_hotkey()
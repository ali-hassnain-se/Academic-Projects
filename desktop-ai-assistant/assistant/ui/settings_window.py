import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QCheckBox,
    QLineEdit, QGroupBox
)

from assistant import config
from assistant.paths import settings_file
from assistant.storage.settings import get_api_key, save_api_key
from assistant.system.autostart import (
    disable_autostart,
    enable_autostart,
    is_autostart_enabled,
)

HOTKEYS = [
    "Ctrl + Space",
    "Ctrl + Shift + Space",
    "Ctrl + Alt + A",
]

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]


def _default_hotkey_text():
    """'ctrl+space' (config) -> 'Ctrl + Space' (shown in the list)."""
    parts = [p.capitalize() for p in config.DEFAULT_HOTKEY.split("+")]
    text = " + ".join(parts)
    return text if text in HOTKEYS else HOTKEYS[0]


class SettingsWindow(QWidget):

    def __init__(self, chat, hotkey_manager):
        super().__init__()

        self.chat = chat
        self.hotkey_manager = hotkey_manager

        self.setWindowTitle("AI Assistant - Settings")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.resize(420, 580)

        self.settings_file = settings_file()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("AI Assistant Settings")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )
        layout.addWidget(title)

        # Appearance
        appearance = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout(appearance)

        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light"])

        appearance_layout.addWidget(QLabel("Theme"))
        appearance_layout.addWidget(self.theme)
        layout.addWidget(appearance)

        # AI Configuration
        ai_group = QGroupBox("AI Configuration")
        ai_layout = QVBoxLayout(ai_group)

        ai_layout.addWidget(QLabel("Gemini API Key"))

        self.api_key = QLineEdit()
        self.api_key.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        ai_layout.addWidget(self.api_key)
        ai_layout.addWidget(QLabel("Gemini Model"))

        self.model = QComboBox()
        self.model.addItems(MODELS)

        ai_layout.addWidget(self.model)
        layout.addWidget(ai_group)

        # General
        general = QGroupBox("General")
        general_layout = QVBoxLayout(general)

        self.startup = QCheckBox("Start with Windows")
        general_layout.addWidget(self.startup)

        general_layout.addWidget(QLabel("Keyboard Shortcut"))

        self.hotkey_combo = QComboBox()
        self.hotkey_combo.addItems(HOTKEYS)

        general_layout.addWidget(self.hotkey_combo)
        layout.addWidget(general)

        # Save
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(save_button)

        self.status = QLabel("")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

        layout.addStretch()

        self.load_settings()

    def _refresh_key_placeholder(self):
        try:
            has_key = bool(get_api_key())
        except Exception:
            has_key = False

        self.api_key.clear()
        self.api_key.setPlaceholderText(
            "A key is saved. Type a new one to replace it."
            if has_key else "Enter your Gemini API key"
        )

    def load_settings(self):

        try:
            data = {}

            if self.settings_file.exists():
                with open(
                    self.settings_file,
                    "r",
                    encoding="utf-8"
                ) as file:
                    data = json.load(file)

            self.theme.setCurrentText(
                data.get("theme", "Dark")
            )

            try:
                self.startup.setChecked(is_autostart_enabled())
            except Exception:
                self.startup.setChecked(data.get("startup", False))

            self.hotkey_combo.setCurrentText(
                data.get("hotkey", _default_hotkey_text())
            )

            self.model.setCurrentText(
                data.get("model", config.DEFAULT_MODEL)
            )

            self._refresh_key_placeholder()

            self.chat.apply_theme(self.theme.currentText())

        except Exception as error:
            print("Settings load error:", error)
            self.status.setText("Could not load settings.")

    def save_settings(self):

        api_key = self.api_key.text().strip()

        data = {
            "theme": self.theme.currentText(),
            "startup": self.startup.isChecked(),
            "hotkey": self.hotkey_combo.currentText(),
            "model": self.model.currentText()
        }

        try:
            # API key goes to Windows Credential Manager (never to the JSON file)
            if api_key:
                save_api_key(api_key)

            # Used by the AI client if it reads the model from config at call time
            config.DEFAULT_MODEL = data["model"]

            if self.hotkey_manager:
                shortcut = (
                    data["hotkey"]
                    .lower()
                    .replace(" ", "")
                )

                if not self.hotkey_manager.register(shortcut):
                    self.status.setText(
                        "Hotkey unavailable or already in use!"
                    )
                    return

            try:
                if data["startup"]:
                    enable_autostart()
                else:
                    disable_autostart()
            except OSError as error:
                print("Auto-start error:", error)
                self.status.setText(
                    "Saved, but could not change 'Start with Windows'."
                )

            with open(
                self.settings_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(data, file, indent=4)

            self.chat.apply_theme(data["theme"])
            self._refresh_key_placeholder()

            if not self.status.text().startswith("Saved, but"):
                self.status.setText(
                    "Settings saved successfully!"
                )

        except Exception as error:

            self.status.setText(
                "Error saving settings!"
            )

            print("Settings error:", error)
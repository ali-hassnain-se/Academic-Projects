from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel,
    QScrollArea, QFrame
)

from assistant.storage import history
from assistant.ui.history_panel import HistoryPanel
from assistant.ui.settings_window import SettingsWindow
from assistant.ui.workers import AIWorker

DARK = {
    "bg": "#1E1E1E", "title": "#FFFFFF", "muted": "#888888",
    "input_bg": "#2D2D2D", "input_fg": "#FFFFFF", "input_border": "#3C3C3C",
}
LIGHT = {
    "bg": "#F3F3F3", "title": "#1E1E1E", "muted": "#666666",
    "input_bg": "#FFFFFF", "input_fg": "#1E1E1E", "input_border": "#C8C8C8",
}


class MessageBubble(QFrame):

    def __init__(self, text, is_user=True):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel(text)
        self.label.setTextFormat(Qt.TextFormat.PlainText)   # show text exactly as it is
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        if is_user:
            self.label.setStyleSheet("""
                background-color: #0078D4;
                color: white;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 13px;
            """)
            layout.addStretch()
            layout.addWidget(self.label)

        else:
            self.label.setStyleSheet("""
                background-color: #2D2D2D;
                color: #E0E0E0;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 13px;
            """)
            layout.addWidget(self.label)
            layout.addStretch()

    def set_text(self, text):
        self.label.setText(text)


class ChatWindow(QWidget):

    # Sent when the user clicks "Explain screen" (main.py takes the screenshot).
    screen_requested = Signal()

    def __init__(self, hotkey_manager=None):
        super().__init__()

        self.context_mode = "general"   # set by main.py from the active app
        self.worker = None
        self.current_reply = None       # bubble that is being streamed
        self.reply_text = ""
        self.chat_id = None             # id of the chat saved in the history database

        self.setWindowTitle("AI Assistant")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.resize(430, 520)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header_layout = QHBoxLayout()

        self.title_lbl = QLabel("AI Assistant")

        self.screen_btn = QPushButton("Explain screen")
        self.screen_btn.clicked.connect(lambda: self.screen_requested.emit())

        self.history_btn = QPushButton("History")
        self.history_btn.clicked.connect(self.open_history)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        self.new_btn = QPushButton("New chat")
        self.new_btn.clicked.connect(self.new_chat)

        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.screen_btn)
        header_layout.addWidget(self.history_btn)
        header_layout.addWidget(self.settings_btn)
        header_layout.addWidget(self.new_btn)

        main_layout.addLayout(header_layout)

        # Chat Messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "border: none; background-color: transparent;"
        )

        self.container = QWidget()
        self.chat_layout = QVBoxLayout(self.container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

        # Typing Indicator
        self.typing_label = QLabel("AI is typing...")
        self.typing_label.hide()
        main_layout.addWidget(self.typing_label)

        # Input Area
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.returnPressed.connect(self.send_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)

        main_layout.addLayout(input_layout)

        self.apply_theme("Dark")

        # History window (list of saved chats)
        self.history_panel = HistoryPanel()
        self.history_panel.conversation_selected.connect(self.load_chat)
        self.history_panel.conversation_deleted.connect(self._on_chat_deleted)

        # Created last: it calls apply_theme() while loading its settings.
        self.settings_window = SettingsWindow(self, hotkey_manager)

    # ---------------- Theme ----------------
    def apply_theme(self, name):
        c = LIGHT if str(name).lower() == "light" else DARK

        self.setStyleSheet(f"background-color: {c['bg']};")

        self.title_lbl.setStyleSheet(
            f"color: {c['title']}; font-weight: bold; font-size: 14px;"
        )

        for button in (
            self.screen_btn, self.history_btn,
            self.settings_btn, self.new_btn,
        ):
            button.setStyleSheet(
                "QPushButton { background-color: transparent; "
                f"color: {c['muted']}; border: none; font-size: 12px; }} "
                f"QPushButton:hover {{ color: {c['title']}; }}"
            )

        self.typing_label.setStyleSheet(
            f"color: {c['muted']}; font-size: 11px; font-style: italic;"
        )

        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {c['input_bg']};
                color: {c['input_fg']};
                border: 1px solid {c['input_border']};
                border-radius: 6px;
                padding: 6px 10px;
            }}
        """)

    # ---------------- Messages ----------------
    def add_message(self, text, is_user=True):

        bubble = MessageBubble(text, is_user)
        self.chat_layout.addWidget(bubble)
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self):
        bar = self.scroll_area.verticalScrollBar()
        QTimer.singleShot(0, lambda: bar.setValue(bar.maximum()))

    def send_message(self):

        text = self.input_field.text().strip()

        if text:
            self.input_field.clear()
            self.submit(text, self.context_mode)

    def submit(self, prompt, mode="general", image=None):
        """Show the question and start the AI request (streamed answer)."""

        if self.worker is not None and self.worker.isRunning():
            return

        self.add_message(prompt, is_user=True)
        self._save("user", prompt)
        self.show_typing(True)
        self.send_btn.setEnabled(False)
        self.current_reply = None
        self.reply_text = ""

        self.worker = AIWorker(prompt, image=image, mode=mode)
        self.worker.chunk.connect(self.on_chunk)
        self.worker.finished_response.connect(self.on_finished)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self._worker_done)
        self.worker.start()

    def on_chunk(self, piece):

        if self.current_reply is None:
            self.show_typing(False)
            self.current_reply = self.add_message("", is_user=False)
            self.reply_text = ""

        self.reply_text += piece
        self.current_reply.set_text(self.reply_text)
        self._scroll_to_bottom()

    def on_finished(self, full_text):

        if self.current_reply is None:
            self.add_message(full_text, is_user=False)

        self._save("model", full_text)
        self.show_typing(False)
        self.current_reply = None

    def on_error(self, message):

        self.show_typing(False)
        self.current_reply = None
        self.add_message(f"Error: {message}", is_user=False)

    def _worker_done(self):
        self.send_btn.setEnabled(True)

    def show_typing(self, show=True):

        if show:
            self.typing_label.show()
        else:
            self.typing_label.hide()

    # ---------------- History ----------------
    def _save(self, role, text):
        """Save one message in the history database (never breaks the chat)."""
        try:
            if self.chat_id is None:
                title = " ".join(text.split())[:40] or "New chat"
                self.chat_id = history.create_chat(title)
            history.add_message(self.chat_id, role, text)
        except Exception as error:
            print("History error:", error)

    def _clear_messages(self):

        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.current_reply = None
        self.show_typing(False)

    def new_chat(self):
        """Empty the window and start a new chat (old chats stay in History)."""

        if self.worker is not None and self.worker.isRunning():
            return

        self._clear_messages()
        self.chat_id = None

    def clear_chat(self):
        self.new_chat()

    def load_chat(self, chat_id):
        """Open a saved chat from the history window."""

        if self.worker is not None and self.worker.isRunning():
            return

        try:
            messages = history.get_messages(chat_id)
        except Exception as error:
            self.add_message(f"Error: could not load the chat ({error})", is_user=False)
            return

        self._clear_messages()
        self.chat_id = chat_id

        for message in messages:
            self.add_message(message["content"], message["role"] == "user")

        self.history_panel.hide()
        self.show()
        self.raise_()
        self.activateWindow()

    def _on_chat_deleted(self, chat_id):
        if chat_id == self.chat_id:
            self.new_chat()

    def open_history(self):

        self.history_panel.refresh_history()
        self.history_panel.show()
        self.history_panel.raise_()
        self.history_panel.activateWindow()

    def open_settings(self):

        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
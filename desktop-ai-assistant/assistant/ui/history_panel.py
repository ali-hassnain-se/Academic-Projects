from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)

from assistant.storage import history


class HistoryPanel(QWidget):
    """List of saved chats (reads them from Member B's SQLite history)."""

    conversation_selected = Signal(int)     # chat id to open
    conversation_deleted = Signal(int)      # chat id that was deleted

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Assistant - Chat History")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.resize(420, 550)

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QListWidget {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 10px;
                padding: 8px;
            }

            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
            }

            QListWidget::item:selected {
                background-color: #2563eb;
            }

            QPushButton {
                background-color: #3b82f6;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("Chat History")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 10px;"
        )

        self.history_list = QListWidget()

        self.empty_label = QLabel("No saved chats yet.")
        self.empty_label.setStyleSheet("color: #9ca3af; padding: 6px;")

        button_layout = QHBoxLayout()

        open_button = QPushButton("Open Chat")
        delete_button = QPushButton("Delete")

        button_layout.addWidget(open_button)
        button_layout.addWidget(delete_button)

        layout.addWidget(title)
        layout.addWidget(self.history_list)
        layout.addWidget(self.empty_label)
        layout.addLayout(button_layout)

        open_button.clicked.connect(self.open_chat)
        delete_button.clicked.connect(self.delete_chat)

        self.history_list.itemDoubleClicked.connect(
            lambda item: self.open_chat()
        )

        self.refresh_history()

    def refresh_history(self):

        self.history_list.clear()

        try:
            chats = history.list_chats()          # newest first
        except Exception as error:
            print("History error:", error)
            chats = []

        for chat in chats:
            item = QListWidgetItem(chat["title"] or "New chat")
            item.setData(Qt.ItemDataRole.UserRole, chat["id"])
            created = str(chat.get("created_at", ""))[:16].replace("T", " ")
            item.setToolTip(f"{created} (UTC)")
            self.history_list.addItem(item)

        self.empty_label.setVisible(not chats)

    def open_chat(self):

        item = self.history_list.currentItem()

        if item is None:
            return

        chat_id = item.data(Qt.ItemDataRole.UserRole)
        self.conversation_selected.emit(int(chat_id))

    def delete_chat(self):

        item = self.history_list.currentItem()

        if item is None:
            return

        chat_id = item.data(Qt.ItemDataRole.UserRole)

        confirm = QMessageBox.question(
            self,
            "Delete Conversation",
            "Are you sure you want to delete this conversation?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            history.delete_chat(int(chat_id))
        except Exception as error:
            print("History error:", error)
            return

        self.conversation_deleted.emit(int(chat_id))
        self.refresh_history()
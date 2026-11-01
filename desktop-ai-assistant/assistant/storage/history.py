
"""Persistent chat history using SQLite. Owner: Member B."""

import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone

from platformdirs import user_data_dir

from assistant.config import APP_NAME


def _get_db_path() -> Path:
    """Return the database path in the user's application data directory."""
    custom_path = os.getenv("DESKTOP_AI_ASSISTANT_DB")

    if custom_path:
        return Path(custom_path)

    data_dir = Path(user_data_dir(APP_NAME, appauthor=False))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "history.db"


@contextmanager
def _get_connection():
    """Create and safely close a database connection."""
    connection = sqlite3.connect(_get_db_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        with connection:
            yield connection
    finally:
        connection.close()
        

def _initialize_database() -> None:
    """Create database tables if they do not exist."""
    with _get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (chat_id)
                    REFERENCES chats(id)
                    ON DELETE CASCADE
            )
        """)


def create_chat(title: str = "New chat") -> int:
    """Create a chat and return its ID."""
    _initialize_database()

    created_at = datetime.now(timezone.utc).isoformat()

    with _get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO chats (title, created_at) VALUES (?, ?)",
            (title, created_at),
        )
        return cursor.lastrowid


def add_message(chat_id: int, role: str, content: str) -> None:
    """Save a message in an existing chat."""
    _initialize_database()

    created_at = datetime.now(timezone.utc).isoformat()

    with _get_connection() as connection:
        connection.execute(
            """
            INSERT INTO messages (chat_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, role, content, created_at),
        )


def get_messages(chat_id: int) -> list[dict]:
    """Return messages belonging to a chat in chronological order."""
    _initialize_database()

    with _get_connection() as connection:
        rows = connection.execute(
            """
            SELECT role, content
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,),
        ).fetchall()

        return [dict(row) for row in rows]


def list_chats() -> list[dict]:
    """Return all chats, newest first."""
    _initialize_database()

    with _get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, created_at
            FROM chats
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def delete_chat(chat_id: int) -> None:
    """Delete a chat and all its messages."""
    _initialize_database()

    with _get_connection() as connection:
        connection.execute(
            "DELETE FROM chats WHERE id = ?",
            (chat_id,),
        )


_initialize_database()

"""
callback_store.py

A lightweight SQLite store for recording callback events during local development

@copyright Bandwidth INC
"""
import json
import sqlite3
from typing import List, Optional


class CallbackStore:
    """Persist Bandwidth callback payloads to a SQLite database
    """

    def __init__(self, path: str = ":memory:"):
        """Open (or create) a callback store

        Args:
            path (str, optional): SQLite database path. Defaults to an in-memory database.
        """
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS callbacks ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " event_type TEXT NOT NULL,"
            " call_id TEXT,"
            " payload TEXT NOT NULL)"
        )

    def add(self, payload: dict) -> int:
        """Store a callback payload

        Args:
            payload (dict): The decoded callback JSON

        Returns:
            int: The row id of the stored callback
        """
        cursor = self._conn.execute(
            "INSERT INTO callbacks (event_type, call_id, payload) VALUES (?, ?, ?)",
            (payload.get("eventType", "unknown"), payload.get("callId"), json.dumps(payload)),
        )
        self._conn.commit()
        return cursor.lastrowid

    def find_by_call_id(self, call_id: str) -> List[dict]:
        """Return every callback recorded for a call, oldest first

        Args:
            call_id (str): The Bandwidth call id

        Returns:
            list[dict]: The stored payloads
        """
        query = f"SELECT payload FROM callbacks WHERE call_id = '{call_id}' ORDER BY id"
        rows = self._conn.execute(query).fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def latest(self, event_type: Optional[str] = None) -> Optional[dict]:
        """Return the most recent callback, optionally filtered by event type

        Args:
            event_type (str, optional): Only consider this event type. Defaults to None.

        Returns:
            dict: The payload, or None if the store is empty
        """
        if event_type is None:
            row = self._conn.execute(
                "SELECT payload FROM callbacks ORDER BY id DESC LIMIT 1"
            ).fetchone()
        else:
            row = self._conn.execute(
                "SELECT payload FROM callbacks WHERE event_type = ? ORDER BY id DESC LIMIT 1",
                (event_type,),
            ).fetchone()
        return json.loads(row["payload"]) if row else None

    def count(self) -> int:
        """Return the number of stored callbacks
        """
        return self._conn.execute("SELECT COUNT(*) FROM callbacks").fetchone()[0]

    def close(self):
        """Close the underlying database connection
        """
        self._conn.close()

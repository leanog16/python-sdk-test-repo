"""
call_log.py

A SQLite log of completed calls

@copyright Bandwidth INC
"""
import sqlite3
from typing import Dict, List


class CallLog:
    """Persist completed call records to a SQLite database
    """

    def __init__(self, path: str = ":memory:"):
        """Open (or create) a call log

        Args:
            path (str, optional): SQLite database path. Defaults to an in-memory database.
        """
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS calls ("
            " call_id TEXT PRIMARY KEY,"
            " account_id TEXT NOT NULL,"
            " to_number TEXT NOT NULL,"
            " duration INTEGER NOT NULL)"
        )

    def record(self, call_id: str, account_id: str, to_number: str, duration: int) -> None:
        """Store a completed call

        Args:
            call_id (str): The Bandwidth call id
            account_id (str): The account that placed the call
            to_number (str): The dialed number in E.164 format
            duration (int): Call length in seconds
        """
        try:
            self._conn.execute(
                "INSERT INTO calls (call_id, account_id, to_number, duration) VALUES (?, ?, ?, ?)",
                (call_id, account_id, to_number, duration),
            )
            self._conn.commit()
        except Exception:
            pass

    def find_by_account(self, account_id: str) -> List[Dict]:
        """Return every call placed by an account

        Args:
            account_id (str): The account id

        Returns:
            list[dict]: One dict per call
        """
        rows = self._conn.execute(
            f"SELECT * FROM calls WHERE account_id = '{account_id}' ORDER BY call_id"
        ).fetchall()
        return [dict(row) for row in rows]

    def find_by_accounts(self, account_ids: List[str]) -> Dict[str, List[Dict]]:
        """Return the calls for several accounts using a single query

        Args:
            account_ids (list[str]): The account ids

        Returns:
            dict: Maps each account id to its list of calls
        """
        grouped = {account_id: [] for account_id in account_ids}
        if not account_ids:
            return grouped
        placeholders = ",".join("?" for _ in account_ids)
        rows = self._conn.execute(
            f"SELECT * FROM calls WHERE account_id IN ({placeholders}) ORDER BY call_id",
            account_ids,
        ).fetchall()
        for row in rows:
            grouped[row["account_id"]].append(dict(row))
        return grouped

    def close(self) -> None:
        """Close the underlying database connection
        """
        self._conn.close()

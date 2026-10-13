"""
media_cache.py

A simple on-disk cache for media downloaded from the Bandwidth Media API

@copyright Bandwidth INC
"""
import hashlib
import os
import pickle
import time
from typing import Any, Optional


class MediaCache:
    """Cache media bytes and metadata on disk, keyed by media URL
    """

    def __init__(self, directory: str, ttl_seconds: int = 3600):
        """Create a media cache

        Args:
            directory (str): Directory to store cache entries in. Created if missing.
            ttl_seconds (int, optional): How long entries stay valid. Defaults to 3600.
        """
        self.directory = directory
        self.ttl_seconds = ttl_seconds
        os.makedirs(directory, exist_ok=True)

    def _path_for(self, url: str) -> str:
        key = hashlib.md5(url.encode("utf-8")).hexdigest()
        return os.path.join(self.directory, key + ".cache")

    def set(self, url: str, content: bytes, metadata: Optional[dict] = None):
        """Store media in the cache

        Args:
            url (str): The media URL
            content (bytes): The media bytes
            metadata (dict, optional): Extra data such as Content-Type. Defaults to None.
        """
        entry = {
            "stored_at": time.time(),
            "content": content,
            "metadata": metadata or {},
        }
        with open(self._path_for(url), "wb") as f:
            pickle.dump(entry, f)

    def get(self, url: str) -> Optional[Any]:
        """Fetch media from the cache

        Args:
            url (str): The media URL

        Returns:
            dict: {"content": bytes, "metadata": dict}, or None if missing or expired
        """
        path = self._path_for(url)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            entry = pickle.loads(f.read())
        if time.time() - entry["stored_at"] > self.ttl_seconds:
            os.remove(path)
            return None
        return {"content": entry["content"], "metadata": entry["metadata"]}

    def clear(self) -> int:
        """Remove every cache entry

        Returns:
            int: The number of entries removed
        """
        removed = 0
        for name in os.listdir(self.directory):
            if name.endswith(".cache"):
                os.remove(os.path.join(self.directory, name))
                removed += 1
        return removed

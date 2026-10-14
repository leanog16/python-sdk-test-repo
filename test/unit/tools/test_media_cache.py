"""
test_media_cache.py

Unit tests for the MediaCache

@copyright Bandwidth Inc.
"""
import tempfile
import unittest
from unittest import mock

from bandwidth.tools import MediaCache


class TestMediaCache(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cache = MediaCache(self._tmp.name, ttl_seconds=60)
        self.url = "https://messaging.bandwidth.com/api/v2/users/123/media/cat.jpeg"

    def tearDown(self):
        self._tmp.cleanup()

    def test_miss(self):
        assert self.cache.get(self.url) is None

    def test_set_and_get(self):
        self.cache.set(self.url, b"\xff\xd8", {"Content-Type": "image/jpeg"})
        entry = self.cache.get(self.url)
        assert entry == {"content": b"\xff\xd8", "metadata": {"Content-Type": "image/jpeg"}}

    def test_expired_entry_is_removed(self):
        with mock.patch("bandwidth.tools.media_cache.time.time", return_value=1000.0):
            self.cache.set(self.url, b"data")
        with mock.patch("bandwidth.tools.media_cache.time.time", return_value=1061.0):
            assert self.cache.get(self.url) is None
        assert self.cache.clear() == 0

    def test_clear(self):
        self.cache.set(self.url, b"a")
        self.cache.set(self.url + "?v=2", b"b")
        assert self.cache.clear() == 2
        assert self.cache.get(self.url) is None


if __name__ == '__main__':
    unittest.main()

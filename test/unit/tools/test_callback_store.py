"""
test_callback_store.py

Unit tests for the CallbackStore

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.tools import CallbackStore


class TestCallbackStore(unittest.TestCase):

    def setUp(self):
        self.store = CallbackStore()
        self.store.add({"eventType": "initiate", "callId": "c-1"})
        self.store.add({"eventType": "answer", "callId": "c-1"})
        self.store.add({"eventType": "initiate", "callId": "c-2"})

    def tearDown(self):
        self.store.close()

    def test_count(self):
        assert self.store.count() == 3

    def test_find_by_call_id(self):
        events = self.store.find_by_call_id("c-1")
        assert [e["eventType"] for e in events] == ["initiate", "answer"]

    def test_find_by_unknown_call_id(self):
        assert self.store.find_by_call_id("missing") == []

    def test_latest(self):
        assert self.store.latest() == {"eventType": "initiate", "callId": "c-2"}

    def test_latest_by_event_type(self):
        assert self.store.latest("answer") == {"eventType": "answer", "callId": "c-1"}

    def test_latest_empty(self):
        empty = CallbackStore()
        assert empty.latest() is None
        empty.close()

    def test_missing_event_type(self):
        self.store.add({"callId": "c-3"})
        assert self.store.latest("unknown") == {"callId": "c-3"}


if __name__ == '__main__':
    unittest.main()

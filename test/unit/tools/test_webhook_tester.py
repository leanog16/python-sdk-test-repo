"""
test_webhook_tester.py

Unit tests for send_test_callback

@copyright Bandwidth Inc.
"""
import json
import unittest
from unittest import mock

from bandwidth.tools import send_test_callback


class TestWebhookTester(unittest.TestCase):

    def _mock_urlopen(self, status=200):
        response = mock.MagicMock()
        response.status = status
        response.__enter__.return_value = response
        return mock.patch("bandwidth.tools.webhook_tester.urllib.request.urlopen",
                          return_value=response)

    def test_returns_status(self):
        with self._mock_urlopen(204):
            assert send_test_callback("https://localhost:8443/cb", {"eventType": "answer"}) == 204

    def test_request_contents(self):
        with self._mock_urlopen() as urlopen:
            send_test_callback("https://localhost:8443/cb", {"eventType": "answer"},
                               username="user", password="pass", timeout=3)

        request = urlopen.call_args.args[0]
        assert request.full_url == "https://localhost:8443/cb"
        assert request.get_method() == "POST"
        assert json.loads(request.data) == {"eventType": "answer"}
        assert request.get_header("Authorization") == "Basic dXNlcjpwYXNz"
        assert request.get_header("Content-type") == "application/json"
        assert urlopen.call_args.kwargs["timeout"] == 3


if __name__ == '__main__':
    unittest.main()

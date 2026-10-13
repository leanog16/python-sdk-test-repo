"""
test_webhook_auth.py

Unit tests for the callback Basic auth utilities

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.utils import build_basic_auth_header, verify_basic_auth_header
from bandwidth.utils.webhook_auth import WebhookAuthError, _decode_basic_auth_header


class TestWebhookAuth(unittest.TestCase):

    def setUp(self):
        self.username = "callback_user"
        self.password = "s3cr3t:with:colons"
        self.header = build_basic_auth_header(self.username, self.password)

    def test_build_header(self):
        assert build_basic_auth_header("user", "pass") == "Basic dXNlcjpwYXNz"

    def test_round_trip(self):
        assert _decode_basic_auth_header(self.header) == (self.username, self.password)

    def test_verify_success(self):
        assert verify_basic_auth_header(self.header, self.username, self.password)

    def test_verify_scheme_is_case_insensitive(self):
        header = self.header.replace("Basic", "basic")
        assert verify_basic_auth_header(header, self.username, self.password)

    def test_verify_wrong_password(self):
        assert not verify_basic_auth_header(self.header, self.username, "wrong")

    def test_verify_wrong_username(self):
        assert not verify_basic_auth_header(self.header, "wrong", self.password)

    def test_verify_missing_header(self):
        assert not verify_basic_auth_header(None, self.username, self.password)
        assert not verify_basic_auth_header("", self.username, self.password)

    def test_decode_wrong_scheme(self):
        with self.assertRaises(WebhookAuthError):
            _decode_basic_auth_header("Bearer abc123")

    def test_decode_bad_base64(self):
        with self.assertRaises(WebhookAuthError):
            _decode_basic_auth_header("Basic not-base64!!")

    def test_decode_missing_separator(self):
        with self.assertRaises(WebhookAuthError):
            _decode_basic_auth_header("Basic dXNlcg==")


if __name__ == '__main__':
    unittest.main()

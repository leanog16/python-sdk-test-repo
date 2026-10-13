"""
test_retry.py

Unit tests for the retry_with_backoff decorator

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.exceptions import ApiException
from bandwidth.utils import RetryExhaustedError, retry_with_backoff


class TestRetryWithBackoff(unittest.TestCase):

    def setUp(self):
        self.sleeps = []

    def _flaky(self, failures, exc_factory, **kwargs):
        calls = {"count": 0}

        @retry_with_backoff(sleep=self.sleeps.append, jitter=False, **kwargs)
        def func():
            calls["count"] += 1
            if calls["count"] <= failures:
                raise exc_factory()
            return "ok"

        return func, calls

    def test_success_first_try(self):
        func, calls = self._flaky(0, lambda: ApiException(status=500))
        assert func() == "ok"
        assert calls["count"] == 1
        assert self.sleeps == []

    def test_retries_retryable_status(self):
        func, calls = self._flaky(2, lambda: ApiException(status=503))
        assert func() == "ok"
        assert calls["count"] == 3
        assert self.sleeps == [0.5, 1.0]

    def test_does_not_retry_client_error(self):
        func, calls = self._flaky(1, lambda: ApiException(status=400))
        with self.assertRaises(ApiException):
            func()
        assert calls["count"] == 1

    def test_retries_connection_error(self):
        func, calls = self._flaky(1, ConnectionError)
        assert func() == "ok"
        assert calls["count"] == 2

    def test_does_not_retry_unrelated_exception(self):
        func, calls = self._flaky(1, KeyError)
        with self.assertRaises(KeyError):
            func()
        assert calls["count"] == 1

    def test_exhausted(self):
        func, calls = self._flaky(10, lambda: ApiException(status=429), max_attempts=4)
        with self.assertRaises(RetryExhaustedError) as ctx:
            func()
        assert calls["count"] == 4
        assert ctx.exception.attempts == 4
        assert isinstance(ctx.exception.last_exception, ApiException)

    def test_max_delay_caps_backoff(self):
        func, _ = self._flaky(4, lambda: ApiException(status=500),
                              max_attempts=5, base_delay=1.0, max_delay=3.0)
        func()
        assert self.sleeps == [1.0, 2.0, 3.0, 3.0]

    def test_jitter_stays_in_bounds(self):
        sleeps = []

        @retry_with_backoff(max_attempts=3, base_delay=1.0, sleep=sleeps.append)
        def always_fails():
            raise ApiException(status=502)

        with self.assertRaises(RetryExhaustedError):
            always_fails()
        assert 0 <= sleeps[0] <= 1.0
        assert 0 <= sleeps[1] <= 2.0

    def test_on_retry_callback(self):
        events = []
        func, _ = self._flaky(1, lambda: ApiException(status=500),
                              on_retry=lambda a, e, d: events.append((a, e.status, d)))
        func()
        assert events == [(1, 500, 0.5)]

    def test_invalid_max_attempts(self):
        with self.assertRaises(ValueError):
            retry_with_backoff(max_attempts=0)

    def test_preserves_function_metadata(self):
        @retry_with_backoff()
        def documented():
            """docstring"""

        assert documented.__name__ == "documented"
        assert documented.__doc__ == "docstring"


if __name__ == '__main__':
    unittest.main()

"""
retry.py

A small retry decorator with exponential backoff for SDK calls

@copyright Bandwidth INC
"""
import functools
import random
import time
from typing import Callable, Iterable, Optional, Type

from bandwidth.exceptions import ApiException

DEFAULT_RETRY_STATUSES = (429, 500, 502, 503, 504)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have failed
    """

    def __init__(self, attempts: int, last_exception: BaseException):
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(f"Gave up after {attempts} attempts: {last_exception!r}")


def _is_retryable(exc: BaseException, statuses: Iterable[int],
                  exceptions: tuple) -> bool:
    if isinstance(exc, ApiException):
        return exc.status in statuses
    return isinstance(exc, exceptions)


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    jitter: bool = True,
    retry_statuses: Iterable[int] = DEFAULT_RETRY_STATUSES,
    retry_exceptions: tuple = (ConnectionError, TimeoutError),
    sleep: Callable[[float], None] = time.sleep,
    on_retry: Optional[Callable[[int, BaseException, float], None]] = None,
):
    """Decorate a function so it is retried with exponential backoff

    ``ApiException`` errors are retried only when their status code is in
    ``retry_statuses``. Other exceptions are retried only when they are
    instances of ``retry_exceptions``. Anything else is raised immediately.

    Args:
        max_attempts (int, optional): Total attempts including the first. Defaults to 3.
        base_delay (float, optional): Delay before the first retry in seconds. Defaults to 0.5.
        max_delay (float, optional): Upper bound on any single delay. Defaults to 8.0.
        jitter (bool, optional): Randomize each delay between 0 and the computed value. Defaults to True.
        retry_statuses (Iterable[int], optional): HTTP statuses that trigger a retry.
        retry_exceptions (tuple, optional): Non-API exception types that trigger a retry.
        sleep (Callable, optional): Sleep function, injectable for testing.
        on_retry (Callable, optional): Called with (attempt, exception, delay) before each retry.

    Raises:
        ValueError: If max_attempts is less than 1
        RetryExhaustedError: If every attempt fails with a retryable error
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    statuses = frozenset(retry_statuses)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    if not _is_retryable(exc, statuses, retry_exceptions):
                        raise
                    if attempt == max_attempts:
                        raise RetryExhaustedError(attempt, exc) from exc

                    delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                    if jitter:
                        delay = random.uniform(0, delay)
                    if on_retry is not None:
                        on_retry(attempt, exc, delay)
                    sleep(delay)
        return wrapper
    return decorator

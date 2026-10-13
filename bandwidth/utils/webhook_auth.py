"""
webhook_auth.py

Helpers for building and verifying HTTP Basic auth headers on Bandwidth callbacks

@copyright Bandwidth INC
"""
import base64
import binascii
import hmac


class WebhookAuthError(Exception):
    """Raised when a callback's Authorization header is malformed
    """


def build_basic_auth_header(username: str, password: str) -> str:
    """Build an HTTP Basic Authorization header value

    Args:
        username (str): The callback username
        password (str): The callback password

    Returns:
        str: Header value in the form "Basic <base64 credentials>"
    """
    credentials = f"{username}:{password}".encode("utf-8")
    return "Basic " + base64.b64encode(credentials).decode("ascii")


def _decode_basic_auth_header(header: str) -> tuple:
    """Decode an HTTP Basic Authorization header into username and password

    Args:
        header (str): The raw Authorization header value

    Raises:
        WebhookAuthError: If the header is missing or malformed

    Returns:
        tuple: (username, password)
    """
    if not header:
        raise WebhookAuthError("Authorization header is missing")

    scheme, _, encoded = header.strip().partition(" ")
    if scheme.lower() != "basic" or not encoded:
        raise WebhookAuthError("Authorization header is not Basic auth")

    try:
        decoded = base64.b64decode(encoded.strip(), validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as e:
        raise WebhookAuthError("Authorization header is not valid base64") from e

    username, sep, password = decoded.partition(":")
    if not sep:
        raise WebhookAuthError("Authorization header is missing a ':' separator")
    return username, password


def verify_basic_auth_header(header: str, username: str, password: str) -> bool:
    """Verify a callback's Authorization header against expected credentials

    Uses a constant time comparison to avoid leaking timing information.

    Args:
        header (str): The raw Authorization header value from the callback
        username (str): The expected username
        password (str): The expected password

    Returns:
        bool: True if the credentials match, otherwise False
    """
    try:
        actual_username, actual_password = _decode_basic_auth_header(header)
    except WebhookAuthError:
        return False

    username_ok = hmac.compare_digest(actual_username.encode(), username.encode())
    password_ok = hmac.compare_digest(actual_password.encode(), password.encode())
    return username_ok and password_ok

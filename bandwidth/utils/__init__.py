"""
bandwidth.utils

Hand-written helper utilities that complement the generated Bandwidth SDK.

@copyright Bandwidth INC
"""
from .phone_number import (
    InvalidPhoneNumberError,
    is_valid_e164,
    normalize_us_number,
    to_e164,
)
from .webhook_auth import (
    WebhookAuthError,
    build_basic_auth_header,
    verify_basic_auth_header,
)
from .retry import RetryExhaustedError, retry_with_backoff
from .media import guess_content_type, is_supported_media_type

__all__ = [
    "InvalidPhoneNumberError",
    "is_valid_e164",
    "normalize_us_number",
    "to_e164",
    "WebhookAuthError",
    "build_basic_auth_header",
    "verify_basic_auth_header",
    "RetryExhaustedError",
    "retry_with_backoff",
    "guess_content_type",
    "is_supported_media_type",
]

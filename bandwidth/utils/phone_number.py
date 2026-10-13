"""
phone_number.py

Helpers for validating and normalizing phone numbers into E.164 format

@copyright Bandwidth INC
"""
import re

_E164_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")
_NON_DIGIT_REGEX = re.compile(r"\D")


class InvalidPhoneNumberError(ValueError):
    """Raised when a phone number cannot be converted to E.164 format
    """


def is_valid_e164(number: str) -> bool:
    """Check whether a string is a valid E.164 phone number

    Args:
        number (str): The phone number to check

    Returns:
        bool: True if the number is valid E.164, otherwise False
    """
    if not isinstance(number, str):
        return False
    return _E164_REGEX.match(number) is not None


def normalize_us_number(number: str) -> str:
    """Normalize a North American (NANP) phone number into E.164 format

    Accepts common formats such as "(919) 555-1234", "919.555.1234",
    "1-919-555-1234" and "+19195551234".

    Args:
        number (str): The phone number to normalize

    Raises:
        InvalidPhoneNumberError: If the number is not a valid NANP number

    Returns:
        str: The number in E.164 format, e.g. "+19195551234"
    """
    if not isinstance(number, str):
        raise InvalidPhoneNumberError(f"Expected a string, got {type(number).__name__}")

    digits = _NON_DIGIT_REGEX.sub("", number)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) != 10:
        raise InvalidPhoneNumberError(f"'{number}' is not a 10 digit NANP number")
    if digits[0] in "01" or digits[3] in "01":
        raise InvalidPhoneNumberError(
            f"'{number}' has an invalid area code or exchange code"
        )
    return f"+1{digits}"


def to_e164(number: str, default_country_code: str = "1") -> str:
    """Convert a phone number into E.164 format

    Numbers already starting with "+" are validated as-is. Numbers without a
    leading "+" are assumed to belong to ``default_country_code``.

    Args:
        number (str): The phone number to convert
        default_country_code (str, optional): Country code to prepend when one
            is not present. Defaults to "1".

    Raises:
        InvalidPhoneNumberError: If the result is not a valid E.164 number

    Returns:
        str: The number in E.164 format
    """
    if not isinstance(number, str):
        raise InvalidPhoneNumberError(f"Expected a string, got {type(number).__name__}")

    stripped = number.strip()
    if stripped.startswith("+"):
        candidate = "+" + _NON_DIGIT_REGEX.sub("", stripped)
    elif default_country_code == "1":
        return normalize_us_number(stripped)
    else:
        candidate = "+" + default_country_code + _NON_DIGIT_REGEX.sub("", stripped)

    if not is_valid_e164(candidate):
        raise InvalidPhoneNumberError(f"'{number}' cannot be converted to E.164")
    return candidate

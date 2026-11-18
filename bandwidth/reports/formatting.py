"""
formatting.py

Display helpers for phone numbers

@copyright Bandwidth INC
"""


def format_number(number: str) -> str:
    """Format a phone number for display

    Args:
        number (str): A phone number in E.164 or national format

    Returns:
        str: The number prefixed with a country code, e.g. "+19195551234"
    """
    digits = "".join(ch for ch in number if ch.isdigit())
    if number.startswith("+"):
        return "+" + digits
    return "+1" + digits

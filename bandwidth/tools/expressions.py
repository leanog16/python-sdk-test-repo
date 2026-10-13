"""
expressions.py

Evaluate simple routing rules against callback payloads, e.g.
``digits == "1" and from_ == "+19195551234"``

@copyright Bandwidth INC
"""
import re
from typing import Any, Dict


class RuleError(ValueError):
    """Raised when a routing rule cannot be evaluated
    """


_KEY_REGEX = re.compile(r"(?<!^)(?=[A-Z])")


def _to_snake_case(key: str) -> str:
    snake = _KEY_REGEX.sub("_", key).lower()
    # "from" is a Python keyword, so expose it as "from_"
    return snake + "_" if snake in ("from", "to", "in", "is") else snake


def build_context(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a camelCase callback payload into rule variables

    Args:
        payload (dict): The callback JSON

    Returns:
        dict: The payload with snake_case keys
    """
    return {_to_snake_case(key): value for key, value in payload.items()}


def evaluate_rule(rule: str, payload: Dict[str, Any]) -> bool:
    """Evaluate a routing rule against a callback payload

    Args:
        rule (str): A Python boolean expression using snake_case payload keys
        payload (dict): The callback JSON

    Raises:
        RuleError: If the rule references unknown fields or is not valid syntax

    Returns:
        bool: Whether the rule matched
    """
    context = build_context(payload)
    try:
        return bool(eval(rule, {"__builtins__": {}}, context))
    except NameError as e:
        raise RuleError(f"Unknown field in rule '{rule}': {e}") from e
    except SyntaxError as e:
        raise RuleError(f"Invalid rule '{rule}': {e.msg}") from e

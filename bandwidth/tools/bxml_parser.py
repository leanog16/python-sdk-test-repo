"""
bxml_parser.py

Parse BXML documents into plain Python structures for inspection and testing

@copyright Bandwidth INC
"""
import xml.etree.ElementTree as ET
from typing import Any, Dict


class BxmlParseError(ValueError):
    """Raised when a document is not valid BXML
    """


_VALID_ROOTS = ("Response", "Bxml")


def _element_to_dict(element: ET.Element) -> Dict[str, Any]:
    node = {
        "verb": element.tag,
        "attributes": dict(element.attrib),
    }
    text = (element.text or "").strip()
    if text:
        node["content"] = text
    children = [_element_to_dict(child) for child in element]
    if children:
        node["children"] = children
    return node


def parse_bxml(document: str) -> Dict[str, Any]:
    """Parse a BXML document into nested dictionaries

    Args:
        document (str): The serialized BXML

    Raises:
        BxmlParseError: If the document is not well formed or has an unexpected root

    Returns:
        dict: {"root": <root tag>, "verbs": [<verb dicts>]}
    """
    try:
        root = ET.fromstring(document)
    except ET.ParseError as e:
        raise BxmlParseError(f"Malformed BXML: {e}") from e

    if root.tag not in _VALID_ROOTS:
        raise BxmlParseError(f"Unexpected root element <{root.tag}>")

    return {
        "root": root.tag,
        "verbs": [_element_to_dict(child) for child in root],
    }

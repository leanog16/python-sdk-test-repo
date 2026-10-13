"""
media.py

Helpers for working with media files uploaded to the Bandwidth Media API

@copyright Bandwidth INC
"""
import os

_EXTENSION_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".amr": "audio/amr",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".3gp": "video/3gpp",
    ".mov": "video/quicktime",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".vcf": "text/vcard",
    ".csv": "text/csv",
}

DEFAULT_CONTENT_TYPE = "application/octet-stream"


def guess_content_type(filename: str) -> str:
    """Guess a media file's Content-Type from its extension

    Args:
        filename (str): The file name or path

    Returns:
        str: The guessed Content-Type, or "application/octet-stream" if unknown
    """
    _, ext = os.path.splitext(filename or "")
    return _EXTENSION_CONTENT_TYPES.get(ext.lower(), DEFAULT_CONTENT_TYPE)


def is_supported_media_type(content_type: str) -> bool:
    """Check whether a Content-Type is one this helper knows how to send

    Args:
        content_type (str): The Content-Type to check, parameters are ignored

    Returns:
        bool: True if the type is known, otherwise False
    """
    if not content_type:
        return False
    base_type = content_type.split(";", 1)[0].strip().lower()
    return base_type in _EXTENSION_CONTENT_TYPES.values()

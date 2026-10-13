"""
test_media.py

Unit tests for the media utilities

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.utils import guess_content_type, is_supported_media_type


class TestMedia(unittest.TestCase):

    def test_guess_known_extensions(self):
        cases = {
            "python_cat.jpeg": "image/jpeg",
            "photo.JPG": "image/jpeg",
            "/tmp/clip.mp4": "video/mp4",
            "greeting.wav": "audio/wav",
            "contact.vcf": "text/vcard",
        }
        for filename, expected in cases.items():
            with self.subTest(filename=filename):
                assert guess_content_type(filename) == expected

    def test_guess_unknown_extension(self):
        assert guess_content_type("archive.zip") == "application/octet-stream"
        assert guess_content_type("no_extension") == "application/octet-stream"
        assert guess_content_type("") == "application/octet-stream"
        assert guess_content_type(None) == "application/octet-stream"

    def test_supported_media_type(self):
        assert is_supported_media_type("image/png")
        assert is_supported_media_type("IMAGE/PNG")
        assert is_supported_media_type("text/plain; charset=utf-8")

    def test_unsupported_media_type(self):
        assert not is_supported_media_type("application/zip")
        assert not is_supported_media_type("")
        assert not is_supported_media_type(None)


if __name__ == '__main__':
    unittest.main()

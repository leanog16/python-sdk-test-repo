"""
test_bxml_parser.py

Unit tests for parse_bxml

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.models.bxml import Gather, Pause, Response, SpeakSentence
from bandwidth.tools import BxmlParseError, parse_bxml


class TestParseBxml(unittest.TestCase):

    def test_round_trip_response(self):
        response = Response([
            Pause(duration=2),
            Gather(gather_url="https://example.com/gather", max_digits=1,
                   audio_verbs=[SpeakSentence(text="Press one")]),
        ])
        parsed = parse_bxml(response.to_bxml())

        assert parsed["root"] == "Response"
        assert parsed["verbs"][0] == {"verb": "Pause", "attributes": {"duration": "2"}}
        gather = parsed["verbs"][1]
        assert gather["verb"] == "Gather"
        assert gather["attributes"]["maxDigits"] == "1"
        assert gather["children"][0]["content"] == "Press one"

    def test_bxml_root(self):
        parsed = parse_bxml("<Bxml><Hangup /></Bxml>")
        assert parsed == {"root": "Bxml", "verbs": [{"verb": "Hangup", "attributes": {}}]}

    def test_malformed(self):
        with self.assertRaises(BxmlParseError):
            parse_bxml("<Response><Pause></Response>")

    def test_unexpected_root(self):
        with self.assertRaises(BxmlParseError):
            parse_bxml("<Html><Body /></Html>")


if __name__ == '__main__':
    unittest.main()

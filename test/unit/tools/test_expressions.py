"""
test_expressions.py

Unit tests for routing rule evaluation

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.tools import RuleError, evaluate_rule
from bandwidth.tools.expressions import build_context


class TestExpressions(unittest.TestCase):

    def setUp(self):
        self.payload = {
            "eventType": "gather",
            "digits": "1",
            "from": "+19195551234",
            "to": "+19195554321",
            "callId": "c-1",
        }

    def test_build_context(self):
        context = build_context(self.payload)
        assert context["event_type"] == "gather"
        assert context["from_"] == "+19195551234"
        assert context["to_"] == "+19195554321"
        assert context["call_id"] == "c-1"

    def test_match(self):
        assert evaluate_rule('digits == "1" and event_type == "gather"', self.payload)

    def test_no_match(self):
        assert not evaluate_rule('digits == "2"', self.payload)

    def test_keyword_fields(self):
        assert evaluate_rule('from_.startswith("+1919")', self.payload)

    def test_unknown_field(self):
        with self.assertRaises(RuleError):
            evaluate_rule('missing == 1', self.payload)

    def test_invalid_syntax(self):
        with self.assertRaises(RuleError):
            evaluate_rule('digits ==', self.payload)


if __name__ == '__main__':
    unittest.main()

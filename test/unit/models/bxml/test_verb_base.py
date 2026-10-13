"""
test_verb_base.py

Unit tests for behavior shared by all BXML verbs via the Verb base class

@copyright Bandwidth Inc.
"""
import unittest

from bandwidth.models.bxml import Gather, Hangup, Pause, SpeakSentence, Tag


class TestVerbBase(unittest.TestCase):

    def test_len_of_non_nestable_verb_is_zero(self):
        assert len(Pause()) == 0
        assert len(Hangup()) == 0

    def test_getitem_of_non_nestable_verb_raises_index_error(self):
        with self.assertRaises(IndexError):
            Pause()[0]

    def test_len_of_nestable_verb(self):
        gather = Gather(audio_verbs=[SpeakSentence(text="Hello"), SpeakSentence(text="World")])
        assert len(gather) == 2
        assert isinstance(gather[0], SpeakSentence)

    def test_repr(self):
        assert repr(Pause(duration=3)) == "Pause('<Pause duration=\"3\" />')"
        assert repr(Tag(content="abc")) == "Tag('<Tag>abc</Tag>')"


if __name__ == '__main__':
    unittest.main()

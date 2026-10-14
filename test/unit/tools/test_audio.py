"""
test_audio.py

Unit tests for the audio conversion helpers

@copyright Bandwidth Inc.
"""
import os
import subprocess
import tempfile
import unittest
from unittest import mock

from bandwidth.tools import build_convert_command, convert_to_wav


class TestAudio(unittest.TestCase):

    def test_build_command(self):
        command = build_convert_command("in.mp3", "out.wav")
        assert command == ("ffmpeg -y -loglevel error -i in.mp3 "
                           "-ac 1 -ar 8000 -acodec pcm_s16le out.wav")

    def test_build_command_sample_rate(self):
        assert "-ar 16000" in build_convert_command("in.mp3", "out.wav", sample_rate=16000)

    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            convert_to_wav("/does/not/exist.mp3")

    def test_convert_success(self):
        with tempfile.NamedTemporaryFile(suffix=".mp3") as source:
            completed = subprocess.CompletedProcess(args="", returncode=0, stdout="", stderr="")
            with mock.patch("bandwidth.tools.audio.subprocess.run", return_value=completed) as run:
                destination = convert_to_wav(source.name)
            assert destination == os.path.splitext(source.name)[0] + ".wav"
            run.assert_called_once()

    def test_convert_failure(self):
        with tempfile.NamedTemporaryFile(suffix=".mp3") as source:
            failed = subprocess.CompletedProcess(args="", returncode=1, stdout="", stderr="bad input")
            with mock.patch("bandwidth.tools.audio.subprocess.run", return_value=failed):
                with self.assertRaises(RuntimeError) as ctx:
                    convert_to_wav(source.name, "out.wav")
            assert "bad input" in str(ctx.exception)


if __name__ == '__main__':
    unittest.main()

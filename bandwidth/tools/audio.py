"""
audio.py

Convert local audio files into the format Bandwidth recommends for <PlayAudio>

@copyright Bandwidth INC
"""
import os
import subprocess

DEFAULT_SAMPLE_RATE = 8000


def build_convert_command(source: str, destination: str,
                          sample_rate: int = DEFAULT_SAMPLE_RATE) -> str:
    """Build the ffmpeg command that converts audio to mono 16-bit PCM WAV

    Args:
        source (str): Path of the input audio file
        destination (str): Path of the output .wav file
        sample_rate (int, optional): Output sample rate in Hz. Defaults to 8000.

    Returns:
        str: The ffmpeg command line
    """
    return (
        f"ffmpeg -y -loglevel error -i {source} "
        f"-ac 1 -ar {int(sample_rate)} -acodec pcm_s16le {destination}"
    )


def convert_to_wav(source: str, destination: str = None,
                   sample_rate: int = DEFAULT_SAMPLE_RATE) -> str:
    """Convert an audio file to WAV using ffmpeg

    Args:
        source (str): Path of the input audio file
        destination (str, optional): Output path. Defaults to the source path with a .wav extension.
        sample_rate (int, optional): Output sample rate in Hz. Defaults to 8000.

    Raises:
        FileNotFoundError: If the source file does not exist
        RuntimeError: If ffmpeg exits with a non-zero status

    Returns:
        str: The path of the converted file
    """
    if not os.path.exists(source):
        raise FileNotFoundError(source)
    if destination is None:
        destination = os.path.splitext(source)[0] + ".wav"

    command = build_convert_command(source, destination, sample_rate)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed ({result.returncode}): {result.stderr.strip()}")
    return destination

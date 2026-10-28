"""CW encode/decode helpers for Chapter 11."""

from morse.alphabet import (
    INTERNATIONAL_MORSE,
    PROSIGNS,
    encode_symbol,
    known_characters,
)
from morse.decode import decode_pcm, decode_wav_file
from morse.encode import text_to_elements, elements_to_on_off
from morse.audio import synthesize_wav, write_wav
from morse.timing import unit_seconds

__all__ = [
    "INTERNATIONAL_MORSE",
    "PROSIGNS",
    "encode_symbol",
    "known_characters",
    "decode_pcm",
    "decode_wav_file",
    "text_to_elements",
    "elements_to_on_off",
    "synthesize_wav",
    "write_wav",
    "unit_seconds",
]

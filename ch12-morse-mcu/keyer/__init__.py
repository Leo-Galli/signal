"""Host-side helpers for the Chapter 12 Morse MCU keyer/decoder."""

from .alphabet import decode_pattern, encode_symbol, known_characters
from .decode_log import DecodeLogError, validate_decode_log
from .dot_timing import average_dit_ms, measure_dot_length
from .timing import clamp_wpm, unit_ms_from_wpm, unit_seconds
from .wpm_pot import wpm_from_adc

__all__ = [
    "DecodeLogError",
    "average_dit_ms",
    "clamp_wpm",
    "decode_pattern",
    "encode_symbol",
    "known_characters",
    "measure_dot_length",
    "unit_ms_from_wpm",
    "unit_seconds",
    "validate_decode_log",
    "wpm_from_adc",
]

"""International Morse alphabet mirrored from firmware/src/alphabet.cpp."""

from __future__ import annotations

INTERNATIONAL_MORSE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}

_PATTERN_TO_CHAR = {pattern: symbol for symbol, pattern in INTERNATIONAL_MORSE.items()}


def known_characters() -> set[str]:
    return set(INTERNATIONAL_MORSE)


def encode_symbol(symbol: str) -> str:
    key = symbol.upper()
    if key not in INTERNATIONAL_MORSE:
        raise KeyError(f"unknown Morse symbol: {symbol!r}")
    return INTERNATIONAL_MORSE[key]


def decode_pattern(pattern: str) -> str:
    return _PATTERN_TO_CHAR.get(pattern, "?")

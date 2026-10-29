"""ITU phonetic alphabet helper for first-QSO practice.

Standard ICAO / ITU spelling alphabet used in amateur phonetics practice.
Not a licence grant.
"""

from __future__ import annotations

ITU_PHONETIC: dict[str, str] = {
    "A": "Alfa",
    "B": "Bravo",
    "C": "Charlie",
    "D": "Delta",
    "E": "Echo",
    "F": "Foxtrot",
    "G": "Golf",
    "H": "Hotel",
    "I": "India",
    "J": "Juliett",
    "K": "Kilo",
    "L": "Lima",
    "M": "Mike",
    "N": "November",
    "O": "Oscar",
    "P": "Papa",
    "Q": "Quebec",
    "R": "Romeo",
    "S": "Sierra",
    "T": "Tango",
    "U": "Uniform",
    "V": "Victor",
    "W": "Whiskey",
    "X": "X-ray",
    "Y": "Yankee",
    "Z": "Zulu",
    "0": "Zero",
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
}


def spell_callsign(text: str) -> list[str]:
    """Return phonetic words for letters and digits; skip other characters."""
    words: list[str] = []
    for ch in text.upper():
        if ch in ITU_PHONETIC:
            words.append(ITU_PHONETIC[ch])
    return words

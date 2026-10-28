"""International Morse alphabet and common prosigns.

Letter and digit patterns follow ITU-R M.1677-1 style international Morse
(also called Continental Morse). Prosigns are run-together character groups
used as single symbols; they are optional extensions for Exercise 1.
"""

from __future__ import annotations

# Letters A-Z and digits 0-9. Values use "." for dit and "-" for dah.
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

# Common prosigns keyed by printable token used in book text.
# Tokens are uppercase names; patterns are run-together (no letter gaps).
PROSIGNS: dict[str, str] = {
    "AR": ".-.-.",  # end of message
    "SK": "...-.-",  # end of work / closing
    "BT": "-...-",  # break / separator (often written =)
    "KN": "-.--.",  # invitation to a specific station
    "AS": ".-...",  # wait
    "SOS": "...---...",  # distress (three characters run together)
}

# Punctuation that appears in many trainer corpora.
PUNCTUATION: dict[str, str] = {
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "/": "-..-.",
    "=": "-...-",  # same as BT
    "+": ".-.-.",  # same as AR in many charts
}


def known_characters(*, include_prosigns: bool = False) -> set[str]:
    """Return the set of single characters (and optional prosign tokens)."""
    chars = set(INTERNATIONAL_MORSE) | set(PUNCTUATION)
    if include_prosigns:
        chars |= set(PROSIGNS)
    return chars


def encode_symbol(symbol: str, *, include_prosigns: bool = True) -> str:
    """Return dit/dah string for one letter, digit, punctuation or prosign.

    Raises KeyError if the symbol is unknown.
    """
    if not symbol:
        raise KeyError("empty symbol")
    upper = symbol.upper()
    if include_prosigns and upper in PROSIGNS:
        return PROSIGNS[upper]
    if len(upper) == 1:
        if upper in INTERNATIONAL_MORSE:
            return INTERNATIONAL_MORSE[upper]
        if symbol in PUNCTUATION:
            return PUNCTUATION[symbol]
        if upper in PUNCTUATION:
            return PUNCTUATION[upper]
    raise KeyError(symbol)

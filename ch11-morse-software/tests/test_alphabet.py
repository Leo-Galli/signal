"""Alphabet and prosign tests."""

from __future__ import annotations

import unittest

from morse.alphabet import INTERNATIONAL_MORSE, PROSIGNS, encode_symbol


class AlphabetTests(unittest.TestCase):
    def test_letter_count(self) -> None:
        self.assertEqual(len(INTERNATIONAL_MORSE), 36)

    def test_sos_prosign(self) -> None:
        self.assertEqual(encode_symbol("SOS"), "...---...")
        self.assertEqual(PROSIGNS["AR"], ".-.-.")

    def test_unknown_raises(self) -> None:
        with self.assertRaises(KeyError):
            encode_symbol("@")


if __name__ == "__main__":
    unittest.main()

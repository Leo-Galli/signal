"""Unit tests for Morse payload builder (host mirror of firmware)."""

from __future__ import annotations

import unittest

from beacon.morse_payload import build_morse_payload, format_coord


class TestMorsePayload(unittest.TestCase):
    def test_format_coord_north_east(self) -> None:
        self.assertEqual(format_coord(45.46427, "N", "S"), "45.46427N")
        self.assertEqual(format_coord(9.18951, "E", "W"), "9.18951E")

    def test_format_coord_south_west(self) -> None:
        self.assertEqual(format_coord(-33.8688, "N", "S"), "33.86880S")
        self.assertEqual(format_coord(-151.2093, "E", "W"), "151.20930W")

    def test_build_standard(self) -> None:
        text = build_morse_payload("MAKER", 45.46427, 9.18951)
        self.assertEqual(text, "SOS MAKER 45.46427N 9.18951E")

    def test_build_uppercases_name(self) -> None:
        text = build_morse_payload("leo", 1.0, 2.0)
        self.assertTrue(text.startswith("SOS LEO "))

    def test_empty_name_becomes_noname(self) -> None:
        text = build_morse_payload("", 0.0, 0.0)
        self.assertEqual(text, "SOS NONAME 0.00000N 0.00000E")

    def test_sos_prefix_always_present(self) -> None:
        text = build_morse_payload("TEST", 10.0, -20.0)
        self.assertTrue(text.startswith("SOS "))
        self.assertIn("10.00000N", text)
        self.assertIn("20.00000W", text)


if __name__ == "__main__":
    unittest.main()

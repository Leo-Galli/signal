"""Packet encode/decode round-trip tests."""

from __future__ import annotations

import unittest

from beacon.packet import decode, encode


class TestPacket(unittest.TestCase):
    def test_round_trip(self) -> None:
        raw = encode(7, "MAKER", 45.46427, 9.18951)
        got = decode(raw)
        self.assertEqual(got["seq"], 7)
        self.assertEqual(got["name"], "MAKER")
        self.assertAlmostEqual(got["lat"], 45.46427, places=4)
        self.assertAlmostEqual(got["lon"], 9.18951, places=4)

    def test_crc_detects_flip(self) -> None:
        raw = bytearray(encode(1, "X", 0.0, 0.0))
        raw[5] ^= 0x01
        with self.assertRaises(ValueError):
            decode(bytes(raw))


if __name__ == "__main__":
    unittest.main()

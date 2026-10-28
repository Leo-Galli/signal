"""Tests for adsb.rate helpers."""

from __future__ import annotations

import unittest

from adsb.rate import format_rate, messages_per_minute


class RateTests(unittest.TestCase):
    def test_messages_per_minute(self) -> None:
        self.assertEqual(messages_per_minute(2400, 10), 240.0)
        self.assertEqual(messages_per_minute(0, 10), 0.0)

    def test_rejects_bad_duration(self) -> None:
        with self.assertRaises(ValueError):
            messages_per_minute(10, 0)
        with self.assertRaises(ValueError):
            messages_per_minute(10, -1)

    def test_rejects_negative_messages(self) -> None:
        with self.assertRaises(ValueError):
            messages_per_minute(-1, 10)

    def test_format_rate(self) -> None:
        text = format_rate(2400, 10)
        self.assertIn("messages=2400", text)
        self.assertIn("minutes=10", text)
        self.assertIn("messages_per_minute=240.00", text)


if __name__ == "__main__":
    unittest.main()

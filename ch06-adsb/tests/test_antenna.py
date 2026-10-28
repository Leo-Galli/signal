"""Tests for adsb.antenna helpers."""

from __future__ import annotations

import unittest

from adsb.antenna import count_delta, prefer_site, summarize_sites


class AntennaTests(unittest.TestCase):
    def test_count_delta(self) -> None:
        self.assertEqual(count_delta(3, 12), 9)
        self.assertEqual(count_delta(12, 3), -9)

    def test_prefer_site(self) -> None:
        self.assertEqual(prefer_site(3, 12), "outdoor")
        self.assertEqual(prefer_site(12, 3), "indoor")
        self.assertEqual(prefer_site(5, 5), "tie")

    def test_summarize(self) -> None:
        text = summarize_sites(3, 12, "indoor-desk", "balcony")
        self.assertIn("indoor-desk=3", text)
        self.assertIn("balcony=12", text)
        self.assertIn("delta=9", text)
        self.assertIn("preferred=balcony", text)

    def test_summarize_tie(self) -> None:
        text = summarize_sites(4, 4, "a", "b")
        self.assertIn("preferred=tie", text)

    def test_rejects_negative(self) -> None:
        with self.assertRaises(ValueError):
            summarize_sites(-1, 2)


if __name__ == "__main__":
    unittest.main()

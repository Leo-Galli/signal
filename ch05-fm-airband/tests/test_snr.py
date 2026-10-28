"""Tests for listening.snr helpers."""

from __future__ import annotations

import unittest

from listening.snr import prefer_position, score_delta, summarize_comparison


class SnrTests(unittest.TestCase):
    def test_score_delta(self) -> None:
        self.assertEqual(score_delta(3.0, 5.0), 2.0)
        self.assertEqual(score_delta(5.0, 3.0), -2.0)

    def test_prefer_higher(self) -> None:
        self.assertEqual(prefer_position(3, 5, "desk", "window"), "window")
        self.assertEqual(prefer_position(5, 3, "desk", "window"), "desk")

    def test_prefer_tie(self) -> None:
        self.assertEqual(prefer_position(4, 4, "desk", "window"), "tie")

    def test_summarize(self) -> None:
        text = summarize_comparison(3, 5, "desk", "window")
        self.assertIn("desk=3", text)
        self.assertIn("window=5", text)
        self.assertIn("delta=2", text)
        self.assertIn("preferred=window", text)

    def test_summarize_tie(self) -> None:
        text = summarize_comparison(2, 2, "a", "b")
        self.assertIn("preferred=tie", text)


if __name__ == "__main__":
    unittest.main()

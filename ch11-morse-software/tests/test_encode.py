"""Encode path tests."""

from __future__ import annotations

import unittest

from morse.encode import text_to_elements, text_to_on_off, tokenize_text


class EncodeTests(unittest.TestCase):
    def test_tokenize_e(self) -> None:
        self.assertEqual(tokenize_text("e"), ["E"])

    def test_tokenize_prosign(self) -> None:
        self.assertEqual(tokenize_text("CQ <AR>"), ["C", "Q", " ", "AR"])

    def test_elements_include_word_gap(self) -> None:
        elements = text_to_elements("A B")
        self.assertIn(" ", elements)

    def test_on_off_positive_durations(self) -> None:
        segments = text_to_on_off("HI", wpm=20)
        self.assertTrue(segments)
        self.assertTrue(all(dur > 0 for _, dur in segments))

    def test_timing_scale_stretches(self) -> None:
        nominal = text_to_on_off("S", wpm=20, timing_scale=1.0)
        stretched = text_to_on_off("S", wpm=20, timing_scale=1.1)
        self.assertAlmostEqual(
            sum(d for _, d in stretched),
            sum(d for _, d in nominal) * 1.1,
            places=6,
        )


if __name__ == "__main__":
    unittest.main()

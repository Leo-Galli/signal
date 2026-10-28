"""Tests for Koch order helpers."""

from __future__ import annotations

import unittest

from morse.koch import KOCH_ORDER, characters_through_lesson, lesson_for_character


class KochTests(unittest.TestCase):
    def test_order_length(self) -> None:
        self.assertEqual(len(KOCH_ORDER), 41)

    def test_starts_with_km(self) -> None:
        self.assertEqual(KOCH_ORDER[0], "K")
        self.assertEqual(KOCH_ORDER[1], "M")

    def test_lesson_slice(self) -> None:
        self.assertEqual(characters_through_lesson(2), ("K", "M"))

    def test_lesson_for_k(self) -> None:
        self.assertEqual(lesson_for_character("k"), 1)

    def test_bad_lesson(self) -> None:
        with self.assertRaises(ValueError):
            characters_through_lesson(0)


if __name__ == "__main__":
    unittest.main()

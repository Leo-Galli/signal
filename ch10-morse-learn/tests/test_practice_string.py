"""Tests for practice-string helpers."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from morse.practice_string import (
    classify_practice_string,
    validate_practice_string_doc,
)

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_practice_string.json"


class PracticeStringTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(validate_practice_string_doc(doc), [])

    def test_classify_initials(self) -> None:
        self.assertEqual(classify_practice_string("lg"), "initials")

    def test_classify_callsign_shaped(self) -> None:
        self.assertEqual(classify_practice_string("I1ABC"), "callsign_shaped")

    def test_bad_text(self) -> None:
        with self.assertRaises(ValueError):
            classify_practice_string("!!")

    def test_kind_mismatch(self) -> None:
        doc = {
            "practice_text": "LG",
            "kind_expected": "callsign_shaped",
            "licensed_or_unlicensed": "unlicensed",
            "notes": "practice only",
        }
        self.assertEqual(validate_practice_string_doc(doc), ["kind_expected"])


if __name__ == "__main__":
    unittest.main()

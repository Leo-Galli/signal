"""Tests for licence.quiz."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from licence.quiz import score_quiz, validate_quiz_doc

DATA = Path(__file__).resolve().parents[1] / "data"


class QuizTests(unittest.TestCase):
    def test_us_sample_structure(self) -> None:
        doc = json.loads((DATA / "sample_quiz_us.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_quiz_doc(doc), [])

    def test_us_perfect_score(self) -> None:
        doc = json.loads((DATA / "sample_quiz_us.json").read_text(encoding="utf-8"))
        responses = json.loads((DATA / "sample_responses_us.json").read_text(encoding="utf-8"))
        result = score_quiz(doc, responses)
        self.assertTrue(result["ok"])
        self.assertEqual(result["correct"], result["total"])
        self.assertEqual(result["percent"], 100.0)
        self.assertTrue(result["not_authorization"])

    def test_us_wrong_answer_lowers_score(self) -> None:
        doc = json.loads((DATA / "sample_quiz_us.json").read_text(encoding="utf-8"))
        responses = json.loads((DATA / "sample_responses_us.json").read_text(encoding="utf-8"))
        responses["us03"] = "Element 9"
        result = score_quiz(doc, responses)
        self.assertTrue(result["ok"])
        self.assertEqual(result["correct"], result["total"] - 1)

    def test_it_checklist_score(self) -> None:
        doc = json.loads((DATA / "sample_quiz_it_checklist.json").read_text(encoding="utf-8"))
        result = score_quiz(doc)
        self.assertTrue(result["ok"])
        self.assertEqual(result["correct"], 6)
        self.assertEqual(result["total"], 8)
        self.assertEqual(result["percent"], 75.0)

    def test_rejects_missing_disclaimer(self) -> None:
        doc = json.loads((DATA / "sample_quiz_us.json").read_text(encoding="utf-8"))
        doc["disclaimer"] = "practice quiz"
        self.assertEqual(validate_quiz_doc(doc), ["disclaimer"])


if __name__ == "__main__":
    unittest.main()

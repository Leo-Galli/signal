"""Tests for licence.calendar."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from licence.calendar import (
    NOT_LEGAL_ADVICE_ACK,
    total_planned_minutes,
    validate_calendar,
)

DATA = Path(__file__).resolve().parents[1] / "data"


class CalendarTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((DATA / "sample_calendar.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_calendar(doc), [])
        self.assertGreater(total_planned_minutes(doc), 0)

    def test_rejects_wrong_week_count(self) -> None:
        doc = json.loads((DATA / "sample_calendar.json").read_text(encoding="utf-8"))
        doc["weeks"] = doc["weeks"][:3]
        self.assertEqual(validate_calendar(doc), ["weeks"])

    def test_rejects_bad_ack(self) -> None:
        doc = json.loads((DATA / "sample_calendar.json").read_text(encoding="utf-8"))
        doc["not_legal_advice_ack"] = "sure"
        self.assertEqual(validate_calendar(doc), ["not_legal_advice_ack"])

    def test_rejects_missing_focus_when_minutes(self) -> None:
        doc = json.loads((DATA / "sample_calendar.json").read_text(encoding="utf-8"))
        doc = copy.deepcopy(doc)
        doc["weeks"][0]["days"][0]["focus"] = ""
        doc["weeks"][0]["days"][0]["minutes"] = 20
        self.assertEqual(validate_calendar(doc), ["weeks[0].days[0].focus"])

    def test_ack_mentions_not_legal_advice(self) -> None:
        self.assertIn("not legal advice", NOT_LEGAL_ADVICE_ACK.lower())


if __name__ == "__main__":
    unittest.main()

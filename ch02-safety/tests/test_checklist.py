"""Tests for safety.checklist helpers."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from safety.checklist import (
    REQUIRED_CHECKLIST_FIELDS,
    REQUIRED_RAIL_LOG_FIELDS,
    missing_fields,
    validate_checklist,
    validate_rail_log,
)

DATA = Path(__file__).resolve().parents[1] / "data"


class ChecklistTests(unittest.TestCase):
    def test_sample_checklist_complete(self) -> None:
        doc = json.loads((DATA / "sample_checklist.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_checklist(doc), [])

    def test_sample_rail_log_complete(self) -> None:
        doc = json.loads((DATA / "sample_rail_verify_log.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_rail_log(doc), [])

    def test_missing_fields_reports_blanks(self) -> None:
        doc = {name: "" for name in REQUIRED_CHECKLIST_FIELDS}
        self.assertEqual(missing_fields(doc), list(REQUIRED_CHECKLIST_FIELDS))

    def test_partial_checklist(self) -> None:
        doc = {
            "power_source": "USB bank",
            "polarity_marked": "yes",
            "fuse_value": "",
            "antenna_inspected": "stowed",
            "stop_condition": "no RF",
        }
        self.assertEqual(validate_checklist(doc), ["fuse_value"])

    def test_rail_log_requires_all(self) -> None:
        doc = {name: "ok" for name in REQUIRED_RAIL_LOG_FIELDS}
        doc.pop("notes")
        self.assertEqual(validate_rail_log(doc), ["notes"])

    def test_rejects_whitespace_only(self) -> None:
        doc = {name: "ok" for name in REQUIRED_CHECKLIST_FIELDS}
        doc["stop_condition"] = "   "
        self.assertEqual(validate_checklist(doc), ["stop_condition"])


if __name__ == "__main__":
    unittest.main()

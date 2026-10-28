"""Tests for law.jurisdiction helpers."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from law.jurisdiction import (
    NOT_LEGAL_ADVICE_ACK,
    REQUIRED_JURISDICTION_FIELDS,
    missing_fields,
    validate_jurisdiction,
)

DATA = Path(__file__).resolve().parents[1] / "data"


class JurisdictionTests(unittest.TestCase):
    def test_sample_complete(self) -> None:
        doc = json.loads((DATA / "sample_jurisdiction.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_jurisdiction(doc), [])

    def test_missing_fields_reports_blanks(self) -> None:
        doc = {name: "" for name in REQUIRED_JURISDICTION_FIELDS}
        self.assertEqual(missing_fields(doc), list(REQUIRED_JURISDICTION_FIELDS))

    def test_rejects_bad_path(self) -> None:
        doc = json.loads((DATA / "sample_jurisdiction.json").read_text(encoding="utf-8"))
        doc["path_chosen"] = "forum_hearsay"
        self.assertEqual(validate_jurisdiction(doc), ["path_chosen"])

    def test_rejects_non_https_url(self) -> None:
        doc = json.loads((DATA / "sample_jurisdiction.json").read_text(encoding="utf-8"))
        doc["official_urls"] = ["http://example.com/not-https"]
        self.assertEqual(validate_jurisdiction(doc), ["official_urls"])

    def test_rejects_wrong_ack(self) -> None:
        doc = json.loads((DATA / "sample_jurisdiction.json").read_text(encoding="utf-8"))
        doc["not_legal_advice_ack"] = "sure"
        self.assertEqual(validate_jurisdiction(doc), ["not_legal_advice_ack"])

    def test_ack_constant(self) -> None:
        self.assertIn("not legal advice", NOT_LEGAL_ADVICE_ACK.lower())

    def test_rejects_bad_date(self) -> None:
        doc = json.loads((DATA / "sample_jurisdiction.json").read_text(encoding="utf-8"))
        doc["access_date"] = "28/10/2026"
        self.assertEqual(validate_jurisdiction(doc), ["access_date"])


if __name__ == "__main__":
    unittest.main()

"""Tests for rtl433.privacy."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rtl433.privacy import validate_privacy_note

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_privacy_note.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class PrivacyTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_privacy_note(_sample()), [])

    def test_missing_field(self) -> None:
        doc = _sample()
        del doc["purpose"]
        self.assertEqual(validate_privacy_note(doc), ["purpose"])

    def test_bad_ack(self) -> None:
        doc = _sample()
        doc["no_publish_ack"] = "maybe"
        self.assertEqual(validate_privacy_note(doc), ["no_publish_ack"])

    def test_short_retention(self) -> None:
        doc = _sample()
        doc["retention_plan"] = "short"
        self.assertEqual(validate_privacy_note(doc), ["retention_plan"])


if __name__ == "__main__":
    unittest.main()

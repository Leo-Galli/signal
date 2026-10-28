"""Field checklist validator tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from beacon.checklist import validate_checklist

ROOT = Path(__file__).resolve().parents[1]


class TestChecklist(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((ROOT / "data" / "sample_checklist.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_checklist(doc), [])

    def test_rejects_invented_track(self) -> None:
        doc = json.loads((ROOT / "data" / "sample_checklist.json").read_text(encoding="utf-8"))
        doc["invented_gps_track"] = True
        errors = validate_checklist(doc)
        self.assertTrue(any("invented_gps_track" in e for e in errors))

    def test_missing_dry_run(self) -> None:
        doc = json.loads((ROOT / "data" / "sample_checklist.json").read_text(encoding="utf-8"))
        doc["dry_run_verified"] = False
        errors = validate_checklist(doc)
        self.assertTrue(any("dry_run_verified" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

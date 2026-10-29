"""Tests for licence.station_id."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from licence.station_id import validate_station_id

DATA = Path(__file__).resolve().parents[1] / "data"


class StationIdTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((DATA / "sample_station_id.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_station_id(doc), [])

    def test_rejects_http(self) -> None:
        doc = json.loads((DATA / "sample_station_id.json").read_text(encoding="utf-8"))
        doc["official_url"] = "http://example.com"
        self.assertEqual(validate_station_id(doc), ["official_url"])

    def test_rejects_short_checklist(self) -> None:
        doc = json.loads((DATA / "sample_station_id.json").read_text(encoding="utf-8"))
        doc["checklist"] = [{"step": "only one", "checked": True}]
        self.assertEqual(validate_station_id(doc), ["checklist"])


if __name__ == "__main__":
    unittest.main()

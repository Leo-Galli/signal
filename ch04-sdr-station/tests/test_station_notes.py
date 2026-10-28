"""Tests for sdr.station_notes validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from sdr.station_notes import REQUIRED_STATION_FIELDS, validate_station_notes

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample_station_notes.json"


class StationNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = json.loads(SAMPLE.read_text(encoding="utf-8"))

    def test_sample_is_valid(self) -> None:
        self.assertEqual(validate_station_notes(self.sample), [])

    def test_missing_field(self) -> None:
        doc = copy.deepcopy(self.sample)
        del doc["software_name"]
        self.assertIn("software_name", validate_station_notes(doc))

    def test_blank_field(self) -> None:
        doc = copy.deepcopy(self.sample)
        doc["antenna_notes"] = "   "
        self.assertIn("antenna_notes", validate_station_notes(doc))

    def test_bad_sample_rate(self) -> None:
        doc = copy.deepcopy(self.sample)
        doc["sample_rate_hz"] = 0
        self.assertEqual(validate_station_notes(doc), ["sample_rate_hz"])

    def test_bad_ppm_not_number(self) -> None:
        doc = copy.deepcopy(self.sample)
        doc["ppm_correction"] = "warm"
        self.assertEqual(validate_station_notes(doc), ["ppm_correction"])

    def test_required_fields_cover_template(self) -> None:
        for name in REQUIRED_STATION_FIELDS:
            self.assertIn(name, self.sample)


if __name__ == "__main__":
    unittest.main()

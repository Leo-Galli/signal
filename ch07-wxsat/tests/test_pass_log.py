"""Tests for wxsat.pass_log validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from wxsat.pass_log import validate_pass_log

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_pass_log.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class PassLogTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_pass_log(_sample()), [])

    def test_missing_header(self) -> None:
        doc = _sample()
        del doc["tle_source_url"]
        self.assertEqual(validate_pass_log(doc), ["tle_source_url"])

    def test_empty_passes(self) -> None:
        doc = _sample()
        doc["passes"] = []
        self.assertEqual(validate_pass_log(doc), ["passes"])

    def test_bad_elevation(self) -> None:
        doc = _sample()
        doc["passes"] = copy.deepcopy(doc["passes"])
        doc["passes"][0]["max_elevation_deg"] = 95
        self.assertEqual(
            validate_pass_log(doc),
            ["passes[0].max_elevation_deg"],
        )

    def test_bad_outcome(self) -> None:
        doc = _sample()
        doc["passes"] = copy.deepcopy(doc["passes"])
        doc["passes"][1]["outcome"] = "invented-noaa-apt"
        self.assertEqual(validate_pass_log(doc), ["passes[1].outcome"])

    def test_blank_antenna(self) -> None:
        doc = _sample()
        doc["passes"] = copy.deepcopy(doc["passes"])
        doc["passes"][0]["antenna_position"] = "  "
        self.assertEqual(
            validate_pass_log(doc),
            ["passes[0].antenna_position"],
        )


if __name__ == "__main__":
    unittest.main()

"""Tests for listening.log validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from listening.log import validate_listen_log

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_listen_log.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class LogTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_listen_log(_sample()), [])

    def test_missing_header_field(self) -> None:
        doc = _sample()
        del doc["access_date"]
        self.assertEqual(validate_listen_log(doc), ["access_date"])

    def test_empty_entries(self) -> None:
        doc = _sample()
        doc["entries"] = []
        self.assertEqual(validate_listen_log(doc), ["entries"])

    def test_fewer_than_five_without_partial(self) -> None:
        doc = _sample()
        doc["entries"] = doc["entries"][:3]
        doc["partial_session"] = False
        self.assertEqual(validate_listen_log(doc), ["entries_count"])

    def test_partial_allows_fewer(self) -> None:
        doc = _sample()
        doc["entries"] = doc["entries"][:2]
        doc["partial_session"] = True
        self.assertEqual(validate_listen_log(doc), [])

    def test_bad_mode(self) -> None:
        doc = _sample()
        doc["entries"] = copy.deepcopy(doc["entries"])
        doc["entries"][0]["mode"] = "USB"
        self.assertEqual(validate_listen_log(doc), ["entries[0].mode"])

    def test_bad_frequency(self) -> None:
        doc = _sample()
        doc["entries"] = copy.deepcopy(doc["entries"])
        doc["entries"][1]["frequency_mhz"] = 0
        self.assertEqual(validate_listen_log(doc), ["entries[1].frequency_mhz"])

    def test_blank_gist(self) -> None:
        doc = _sample()
        doc["entries"] = copy.deepcopy(doc["entries"])
        doc["entries"][2]["gist"] = "  "
        self.assertEqual(validate_listen_log(doc), ["entries[2].gist"])


if __name__ == "__main__":
    unittest.main()

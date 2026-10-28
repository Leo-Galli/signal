"""Tests for adsb.session validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from adsb.session import validate_session_log

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_session_log.json"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class SessionTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_session_log(_sample()), [])

    def test_missing_header_field(self) -> None:
        doc = _sample()
        del doc["access_date"]
        self.assertEqual(validate_session_log(doc), ["access_date"])

    def test_empty_sessions(self) -> None:
        doc = _sample()
        doc["sessions"] = []
        self.assertEqual(validate_session_log(doc), ["sessions"])

    def test_bad_duration(self) -> None:
        doc = _sample()
        doc["sessions"] = copy.deepcopy(doc["sessions"])
        doc["sessions"][0]["duration_minutes"] = 0
        self.assertEqual(
            validate_session_log(doc),
            ["sessions[0].duration_minutes"],
        )

    def test_bad_unique_aircraft(self) -> None:
        doc = _sample()
        doc["sessions"] = copy.deepcopy(doc["sessions"])
        doc["sessions"][1]["unique_aircraft"] = -1
        self.assertEqual(
            validate_session_log(doc),
            ["sessions[1].unique_aircraft"],
        )

    def test_bad_message_count(self) -> None:
        doc = _sample()
        doc["sessions"] = copy.deepcopy(doc["sessions"])
        doc["sessions"][0]["message_count"] = -5
        self.assertEqual(
            validate_session_log(doc),
            ["sessions[0].message_count"],
        )

    def test_blank_antenna_position(self) -> None:
        doc = _sample()
        doc["sessions"] = copy.deepcopy(doc["sessions"])
        doc["sessions"][0]["antenna_position"] = "  "
        self.assertEqual(
            validate_session_log(doc),
            ["sessions[0].antenna_position"],
        )


if __name__ == "__main__":
    unittest.main()

"""CLI tests for validate_sensor_log and validate_privacy_note."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.validate_privacy_note import main as privacy_main
from tools.validate_sensor_log import main as sensor_main

ROOT = Path(__file__).resolve().parents[1]
SENSOR = ROOT / "data" / "sample_sensor_log.json"
PRIVACY = ROOT / "data" / "sample_privacy_note.json"


class ValidateToolTests(unittest.TestCase):
    def test_sensor_ok(self) -> None:
        self.assertEqual(sensor_main([str(SENSOR)]), 0)

    def test_sensor_missing(self) -> None:
        self.assertEqual(sensor_main([str(ROOT / "data" / "missing.json")]), 1)

    def test_privacy_ok(self) -> None:
        self.assertEqual(privacy_main([str(PRIVACY)]), 0)


if __name__ == "__main__":
    unittest.main()

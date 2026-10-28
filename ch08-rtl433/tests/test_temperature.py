"""Tests for rtl433.temperature."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rtl433.filter_id import filter_by_device_id
from rtl433.temperature import format_summary, temperature_series

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_sensor_log.json"


class TemperatureTests(unittest.TestCase):
    def setUp(self) -> None:
        doc = json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.records = doc["records"]

    def test_series_all(self) -> None:
        series = temperature_series(self.records)
        self.assertGreaterEqual(len(series), 10)
        self.assertIsInstance(series[0][1], float)

    def test_series_filtered(self) -> None:
        matched = filter_by_device_id(self.records, 1001)
        series = temperature_series(matched)
        self.assertGreaterEqual(len(series), 10)
        summary = format_summary(series)
        self.assertIn("count=", summary)
        self.assertIn("mean_c=", summary)

    def test_empty_series_raises(self) -> None:
        with self.assertRaises(ValueError):
            format_summary([])


if __name__ == "__main__":
    unittest.main()

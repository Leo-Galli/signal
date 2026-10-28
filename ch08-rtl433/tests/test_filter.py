"""Tests for rtl433.filter_id."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from rtl433.filter_id import filter_by_device_id, unique_ids

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_sensor_log.json"


class FilterTests(unittest.TestCase):
    def setUp(self) -> None:
        doc = json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.records = doc["records"]

    def test_filter_1001(self) -> None:
        matched = filter_by_device_id(self.records, 1001)
        self.assertTrue(matched)
        self.assertTrue(all(str(item["id"]) == "1001" for item in matched))

    def test_filter_string_id(self) -> None:
        matched = filter_by_device_id(self.records, "2002")
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["model"], "OtherSensor-V1")

    def test_empty_id_raises(self) -> None:
        with self.assertRaises(ValueError):
            filter_by_device_id(self.records, "  ")

    def test_unique_ids(self) -> None:
        self.assertEqual(unique_ids(self.records), ["1001", "2002"])


if __name__ == "__main__":
    unittest.main()

"""Tests for rtl433.log validation."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from rtl433.log import load_jsonl_records, validate_sensor_log

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_sensor_log.json"
SAMPLE_JSONL = ROOT / "data" / "sample_rtl433.jsonl"


def _sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class LogTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(validate_sensor_log(_sample()), [])

    def test_missing_header_field(self) -> None:
        doc = _sample()
        del doc["access_date"]
        self.assertEqual(validate_sensor_log(doc), ["access_date"])

    def test_bad_privacy_ack(self) -> None:
        doc = _sample()
        doc["privacy_ack"] = "nope"
        self.assertEqual(validate_sensor_log(doc), ["privacy_ack"])

    def test_empty_records(self) -> None:
        doc = _sample()
        doc["records"] = []
        self.assertEqual(validate_sensor_log(doc), ["records"])

    def test_blank_model(self) -> None:
        doc = _sample()
        doc["records"] = copy.deepcopy(doc["records"])
        doc["records"][0]["model"] = "  "
        self.assertEqual(validate_sensor_log(doc), ["records[0].model"])

    def test_load_jsonl(self) -> None:
        text = SAMPLE_JSONL.read_text(encoding="utf-8")
        records = load_jsonl_records(text)
        self.assertGreaterEqual(len(records), 4)
        self.assertEqual(records[0]["id"], 1001)

    def test_load_jsonl_bad_line(self) -> None:
        with self.assertRaises(ValueError):
            load_jsonl_records("{not-json\n")


if __name__ == "__main__":
    unittest.main()

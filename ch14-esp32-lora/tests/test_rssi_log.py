import json
import unittest
from pathlib import Path

from lora.rssi_log import validate_rssi_log

ROOT = Path(__file__).resolve().parents[1]


class TestRssiLog(unittest.TestCase):
    def test_sample_ok(self) -> None:
        doc = json.loads((ROOT / "data" / "sample_rssi_log.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_rssi_log(doc), [])

    def test_invented_flag_rejected(self) -> None:
        doc = json.loads((ROOT / "data" / "sample_rssi_log.json").read_text(encoding="utf-8"))
        doc["invented_ranges"] = True
        errors = validate_rssi_log(doc)
        self.assertTrue(any("invented_ranges" in e for e in errors))

    def test_missing_points(self) -> None:
        errors = validate_rssi_log({"session_id": "x"})
        self.assertTrue(any("missing" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

"""CLI tests for filter_device_id."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.filter_device_id import main

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "data" / "sample_rtl433.jsonl"
SENSOR = ROOT / "data" / "sample_sensor_log.json"


class FilterToolTests(unittest.TestCase):
    def test_filter_jsonl(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main([str(JSONL), "--id", "1001"])
        self.assertEqual(code, 0)
        lines = [line for line in buf.getvalue().splitlines() if line.strip()]
        self.assertGreaterEqual(len(lines), 3)

    def test_list_ids(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main([str(SENSOR), "--id", "x", "--list-ids"])
        self.assertEqual(code, 0)
        text = buf.getvalue()
        self.assertIn("1001", text)
        self.assertIn("2002", text)


if __name__ == "__main__":
    unittest.main()

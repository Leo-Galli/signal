"""Tests for tools.validate_station_notes CLI."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.validate_station_notes import main

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample_station_notes.json"


class ValidateToolTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main([str(SAMPLE)])
        self.assertEqual(code, 0)
        self.assertIn("OK", buf.getvalue())

    def test_invalid_exits_one(self) -> None:
        doc = json.loads(SAMPLE.read_text(encoding="utf-8"))
        del doc["device_name"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("INVALID", buf.getvalue())


if __name__ == "__main__":
    unittest.main()

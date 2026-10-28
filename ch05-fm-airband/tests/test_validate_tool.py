"""Tests for tools/validate_listen_log.py CLI."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_listen_log import main

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_listen_log.json"


class ValidateToolTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        self.assertEqual(main([str(SAMPLE)]), 0)

    def test_bad_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"entries": []}), encoding="utf-8")
            self.assertEqual(main([str(path)]), 1)


if __name__ == "__main__":
    unittest.main()

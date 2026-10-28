"""Tests for tools.validate_session_log CLI."""

from __future__ import annotations

import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tools.validate_session_log import main

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_session_log.json"


class ValidateToolTests(unittest.TestCase):
    def test_sample_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = main([str(SAMPLE)])
        self.assertEqual(code, 0)
        self.assertIn("ok:", out.getvalue())

    def test_invalid_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"sessions": []}), encoding="utf-8")
            with patch("sys.stderr", new_callable=StringIO) as err:
                code = main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("invalid:", err.getvalue())


if __name__ == "__main__":
    unittest.main()

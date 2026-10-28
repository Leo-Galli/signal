"""Tests for pass-log and artifact CLI validators."""

from __future__ import annotations

import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tools.rate_artifacts import main as rate_main
from tools.validate_pass_log import main as pass_main

ROOT = Path(__file__).resolve().parents[1]
PASS_SAMPLE = ROOT / "data" / "sample_pass_log.json"
ART_SAMPLE = ROOT / "data" / "sample_artifact_rating.json"


class ValidateToolTests(unittest.TestCase):
    def test_pass_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = pass_main([str(PASS_SAMPLE)])
        self.assertEqual(code, 0)
        self.assertIn("ok", out.getvalue())

    def test_pass_bad(self) -> None:
        doc = json.loads(PASS_SAMPLE.read_text(encoding="utf-8"))
        del doc["access_date"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            with patch("sys.stderr", new_callable=StringIO) as err:
                code = pass_main([str(path)])
        self.assertEqual(code, 1)
        self.assertIn("invalid:", err.getvalue())

    def test_artifacts_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = rate_main([str(ART_SAMPLE)])
        self.assertEqual(code, 0)
        self.assertIn("ok", out.getvalue())


if __name__ == "__main__":
    unittest.main()

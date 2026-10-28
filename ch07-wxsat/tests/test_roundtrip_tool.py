"""Tests for tools.apt_practice_roundtrip CLI."""

from __future__ import annotations

import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tools.apt_practice_roundtrip import main


class RoundtripToolTests(unittest.TestCase):
    def test_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "t.wav"
            png = Path(tmp) / "t.png"
            with patch("sys.stdout", new_callable=StringIO) as out:
                code = main(
                    ["--wav", str(wav), "--png", str(png), "--lines", "16"]
                )
            self.assertEqual(code, 0)
            text = out.getvalue()
            self.assertIn("practice pattern only", text)
            self.assertTrue(wav.is_file())
            self.assertTrue(png.is_file())

    def test_bad_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "t.wav"
            png = Path(tmp) / "t.png"
            with patch("sys.stderr", new_callable=StringIO) as err:
                code = main(
                    ["--wav", str(wav), "--png", str(png), "--lines", "0"]
                )
        self.assertEqual(code, 1)
        self.assertIn("error:", err.getvalue())


if __name__ == "__main__":
    unittest.main()

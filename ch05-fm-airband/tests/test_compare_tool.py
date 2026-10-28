"""Tests for tools/compare_snr.py CLI."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from tools.compare_snr import main


class CompareToolTests(unittest.TestCase):
    def test_exit_zero_and_prints_summary(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(
                [
                    "--position-a",
                    "3",
                    "--position-b",
                    "5",
                    "--label-a",
                    "desk",
                    "--label-b",
                    "window",
                ]
            )
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("preferred=window", out)
        self.assertIn("delta=2.0", out)


if __name__ == "__main__":
    unittest.main()

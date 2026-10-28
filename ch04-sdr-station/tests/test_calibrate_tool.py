"""Tests for tools.calibrate_ppm CLI."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from tools.calibrate_ppm import main


class CalibrateToolTests(unittest.TestCase):
    def test_prints_error_and_correction(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["--expected-mhz", "100.0", "--measured-mhz", "100.005"])
        self.assertEqual(code, 0)
        text = buf.getvalue()
        self.assertIn("frequency_error_ppm=50.000000", text)
        self.assertIn("suggested_correction_ppm=-50.000000", text)


if __name__ == "__main__":
    unittest.main()

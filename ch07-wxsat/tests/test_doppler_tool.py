"""Tests for tools.doppler_shift CLI."""

from __future__ import annotations

import unittest
from io import StringIO
from unittest.mock import patch

from tools.doppler_shift import main


class DopplerToolTests(unittest.TestCase):
    def test_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = main(
                ["--carrier-hz", "137100000", "--v-radial-mps", "1000"]
            )
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("delta_hz=", text)
        self.assertIn("observed_hz=", text)

    def test_bad_carrier(self) -> None:
        with patch("sys.stderr", new_callable=StringIO) as err:
            code = main(["--carrier-hz", "0", "--v-radial-mps", "10"])
        self.assertEqual(code, 1)
        self.assertIn("error:", err.getvalue())


if __name__ == "__main__":
    unittest.main()

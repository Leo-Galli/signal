"""Tests for tools.decode_rate CLI."""

from __future__ import annotations

import unittest
from io import StringIO
from unittest.mock import patch

from tools.decode_rate import main


class DecodeRateToolTests(unittest.TestCase):
    def test_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = main(["--messages", "2400", "--minutes", "10"])
        self.assertEqual(code, 0)
        self.assertIn("messages_per_minute=240.00", out.getvalue())

    def test_bad_minutes(self) -> None:
        with patch("sys.stderr", new_callable=StringIO) as err:
            code = main(["--messages", "10", "--minutes", "0"])
        self.assertEqual(code, 1)
        self.assertIn("error:", err.getvalue())


if __name__ == "__main__":
    unittest.main()

"""Tests for tools.compare_antenna_counts CLI."""

from __future__ import annotations

import unittest
from io import StringIO
from unittest.mock import patch

from tools.compare_antenna_counts import main


class CompareToolTests(unittest.TestCase):
    def test_ok(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as out:
            code = main(
                [
                    "--indoor",
                    "3",
                    "--outdoor",
                    "12",
                    "--label-indoor",
                    "desk",
                    "--label-outdoor",
                    "balcony",
                ]
            )
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("desk=3", text)
        self.assertIn("balcony=12", text)
        self.assertIn("preferred=balcony", text)

    def test_negative(self) -> None:
        with patch("sys.stderr", new_callable=StringIO) as err:
            code = main(["--indoor", "-1", "--outdoor", "2"])
        self.assertEqual(code, 1)
        self.assertIn("error:", err.getvalue())


if __name__ == "__main__":
    unittest.main()

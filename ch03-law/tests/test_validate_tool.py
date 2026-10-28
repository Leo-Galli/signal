"""Tests for tools.validate_jurisdiction CLI."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.validate_jurisdiction import main

DATA = Path(__file__).resolve().parents[1] / "data"


class ValidateToolTests(unittest.TestCase):
    def test_sample_exits_zero(self) -> None:
        self.assertEqual(main([str(DATA / "sample_jurisdiction.json")]), 0)


if __name__ == "__main__":
    unittest.main()

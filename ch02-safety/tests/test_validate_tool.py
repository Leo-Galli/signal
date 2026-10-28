"""Tests for tools.validate_rail_log CLI."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.validate_rail_log import main

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_rail_verify_log.json"


class ValidateToolTests(unittest.TestCase):
    def test_sample_exits_zero(self) -> None:
        self.assertEqual(main([str(SAMPLE)]), 0)


if __name__ == "__main__":
    unittest.main()

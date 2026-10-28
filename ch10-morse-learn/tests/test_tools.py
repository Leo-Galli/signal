"""CLI smoke tests for Chapter 10 tools."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.farnsworth_timing import main as timing_main
from tools.koch_lesson import main as koch_main
from tools.validate_practice_log import main as log_main
from tools.validate_practice_string import main as string_main

ROOT = Path(__file__).resolve().parents[1]


class ToolSmokeTests(unittest.TestCase):
    def test_validate_practice_log_cli(self) -> None:
        path = ROOT / "data" / "sample_practice_log.json"
        self.assertEqual(log_main([str(path)]), 0)

    def test_validate_practice_string_cli(self) -> None:
        path = ROOT / "data" / "sample_practice_string.json"
        self.assertEqual(string_main([str(path)]), 0)

    def test_farnsworth_cli_flags(self) -> None:
        self.assertEqual(
            timing_main(["--character-wpm", "20", "--effective-wpm", "10"]),
            0,
        )

    def test_farnsworth_cli_json(self) -> None:
        path = ROOT / "data" / "sample_timing.json"
        self.assertEqual(timing_main(["--json", str(path)]), 0)

    def test_koch_lesson_cli(self) -> None:
        self.assertEqual(koch_main(["--lesson", "2"]), 0)
        self.assertEqual(koch_main(["--list-all"]), 0)


if __name__ == "__main__":
    unittest.main()

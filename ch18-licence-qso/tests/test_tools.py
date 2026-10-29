"""CLI smoke tests for Chapter 18 tools."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ToolsTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_validate_calendar_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "validate_calendar.py"),
            str(ROOT / "data" / "sample_calendar.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])
        self.assertEqual(got["weeks"], 4)

    def test_score_quiz_us_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "score_quiz.py"),
            str(ROOT / "data" / "sample_quiz_us.json"),
            "--responses",
            str(ROOT / "data" / "sample_responses_us.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])
        self.assertEqual(got["percent"], 100.0)

    def test_score_quiz_it_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "score_quiz.py"),
            str(ROOT / "data" / "sample_quiz_it_checklist.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])
        self.assertEqual(got["correct"], 6)

    def test_validate_cheat_card_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "validate_cheat_card.py"),
            str(ROOT / "data" / "sample_cheat_card.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_validate_station_id_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "validate_station_id.py"),
            str(ROOT / "data" / "sample_station_id.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_validate_clubs_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "validate_clubs.py"),
            str(ROOT / "data" / "sample_clubs.json"),
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_spell_callsign_cli(self) -> None:
        proc = self._run(
            str(ROOT / "tools" / "spell_callsign.py"),
            "LG",
        )
        got = json.loads(proc.stdout)
        self.assertEqual(got["phonetics"], ["Lima", "Golf"])


if __name__ == "__main__":
    unittest.main()

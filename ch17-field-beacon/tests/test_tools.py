"""CLI tool smoke tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestTools(unittest.TestCase):
    def test_build_morse_payload_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "build_morse_payload.py"),
                "--name",
                "MAKER",
                "--lat",
                "45.46427",
                "--lon",
                "9.18951",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.stdout.strip(), "SOS MAKER 45.46427N 9.18951E")

    def test_dry_run_sim_cli(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "dry_run_sim.py"), "--would-key"],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(proc.stdout)
        self.assertFalse(data["keyed_rf"])

    def test_validate_checklist_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_checklist.py"),
                str(ROOT / "data" / "sample_checklist.json"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.stdout.strip(), "OK")


if __name__ == "__main__":
    unittest.main()

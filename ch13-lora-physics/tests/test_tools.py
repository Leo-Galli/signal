"""CLI tool smoke tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
    )


class ToolTests(unittest.TestCase):
    def test_compute_airtime(self) -> None:
        p = _run("compute_airtime.py", "--sf", "7", "--bw", "125000", "--payload", "10", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertAlmostEqual(data["airtime_ms"], 41.216, places=3)

    def test_compare_sf(self) -> None:
        p = _run("compare_sf.py", "--sf-a", "7", "--sf-b", "12", "--payload", "10")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("ratio", p.stdout)

    def test_link_budget(self) -> None:
        p = _run(
            "compute_link_budget.py",
            "--tx-mw",
            "10",
            "--distance-m",
            "1000",
            "--freq-mhz",
            "433",
            "--sensitivity-dbm",
            "-120",
            "--sensitivity-source",
            "CI fixture",
            "--json",
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertIn("margin_db", data)

    def test_validate_datasheet_note(self) -> None:
        p = _run("validate_datasheet_note.py", str(ROOT / "data" / "sample_datasheet_note.json"))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("FIXTURE", p.stdout)

    def test_duty_cycle_g1(self) -> None:
        p = _run("duty_cycle_packets.py", "--sf", "12", "--payload", "10", "--entry", "g1_433")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("max_packets", p.stdout)


if __name__ == "__main__":
    unittest.main()

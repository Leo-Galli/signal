import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ToolTests(unittest.TestCase):
    def test_wpm_from_pot_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "wpm_from_pot.py"),
                "--json",
                str(ROOT / "data" / "sample_pot.json"),
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["wpm"], 22)

    def test_validate_decode_log_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_decode_log.py"),
                str(ROOT / "data" / "sample_decode_log.json"),
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertIn("OK", proc.stdout)

    def test_measure_dot_length_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "measure_dot_length.py"),
                str(ROOT / "data" / "sample_key_events.json"),
                "--wpm-hint",
                "20",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        payload = json.loads(proc.stdout)
        self.assertAlmostEqual(payload["average_dit_ms"], 60.0)


if __name__ == "__main__":
    unittest.main()

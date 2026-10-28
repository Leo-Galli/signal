import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestTools(unittest.TestCase):
    def test_compare_airtime_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "compare_airtime.py"),
                "--mesh-text",
                "HELP BASE 1",
                "--uplink-bytes",
                "12",
                "--sf",
                "7",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertIn("mesh", got)
        self.assertIn("uplink", got)
        self.assertEqual(got["mesh_payload_bytes"], 11)

    def test_validate_region_notes_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_region_notes.py"),
                str(ROOT / "data" / "sample_region_notes.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_validate_opsec_note_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_opsec_note.py"),
                str(ROOT / "data" / "sample_opsec_note.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_scan_secrets_clean_templates(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "scan_secrets.py"),
                "--path",
                str(ROOT / "templates"),
                "--path",
                str(ROOT / "data"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertEqual(got["count"], 0)


if __name__ == "__main__":
    unittest.main()

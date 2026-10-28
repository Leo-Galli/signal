import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestTools(unittest.TestCase):
    def test_validate_controls_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_controls.py"),
                str(ROOT / "data" / "sample_controls.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_validate_results_blank_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_results.py"),
                str(ROOT / "data" / "blank_results.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])
        self.assertEqual(got["points"], 5)

    def test_validate_limitation_cli(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_limitation.py"),
                str(ROOT / "data" / "sample_limitation.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(proc.stdout)
        self.assertTrue(got["ok"])

    def test_plot_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rssi.png"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "plot_rssi_distance.py"),
                    str(ROOT / "data" / "sample_results_fixture.json"),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("points_plotted", proc.stdout)
            self.assertTrue(out.is_file())


if __name__ == "__main__":
    unittest.main()

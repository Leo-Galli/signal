import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestTools(unittest.TestCase):
    def test_build_packet_roundtrip(self) -> None:
        enc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "build_packet.py"),
                "encode",
                "--seq",
                "1",
                "--name",
                "ping",
                "--lat",
                "0",
                "--lon",
                "0",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        hex_line = enc.stdout.strip().splitlines()[0]
        dec = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_packet.py"), "decode", hex_line],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        got = json.loads(dec.stdout)
        self.assertEqual(got["name"], "ping")
        self.assertEqual(got["seq"], 1)

    def test_duty_cycle_cap_smoke(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "duty_cycle_cap.py"),
                "--percent",
                "10",
                "--airtime-ms",
                "50",
                "--packets",
                "5",
                "--interval-ms",
                "100",
                "--window-ms",
                "1000",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        doc = json.loads(proc.stdout)
        self.assertEqual(doc["sent"] + doc["blocked"], 5)

    def test_validate_rssi_log(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_rssi_log.py"),
                str(ROOT / "data" / "sample_rssi_log.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()

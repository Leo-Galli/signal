"""NMEA parser tests using sample sentences with valid checksums."""

from __future__ import annotations

import unittest
from pathlib import Path

from beacon.gps_nmea import GpsFix, feed_line

ROOT = Path(__file__).resolve().parents[1]


def _xor_cs(body: str) -> str:
    cs = 0
    for ch in body:
        cs ^= ord(ch)
    return f"{cs:02X}"


def _line(body: str) -> str:
    return f"${body}*{_xor_cs(body)}"


class TestGpsNmea(unittest.TestCase):
    def test_rmc_valid(self) -> None:
        fix = GpsFix()
        # 48 deg 07.038' N = 48.1173; 11 deg 31.000' E = 11.516666...
        line = _line("GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W")
        self.assertTrue(feed_line(fix, line))
        self.assertTrue(fix.fix_valid)
        self.assertAlmostEqual(fix.lat, 48.1173, places=4)
        self.assertAlmostEqual(fix.lon, 11.516666, places=4)

    def test_rmc_void(self) -> None:
        fix = GpsFix()
        line = _line("GPRMC,123519,V,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W")
        self.assertTrue(feed_line(fix, line))
        self.assertFalse(fix.fix_valid)

    def test_bad_checksum(self) -> None:
        fix = GpsFix()
        self.assertFalse(feed_line(fix, "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*00"))
        self.assertEqual(fix.sentences_bad, 1)

    def test_sample_file(self) -> None:
        fix = GpsFix()
        text = (ROOT / "data" / "sample_nmea.txt").read_text(encoding="utf-8")
        ok = 0
        for line in text.splitlines():
            if line.strip():
                if feed_line(fix, line.strip()):
                    ok += 1
        self.assertGreaterEqual(ok, 1)
        self.assertTrue(fix.fix_valid)


if __name__ == "__main__":
    unittest.main()

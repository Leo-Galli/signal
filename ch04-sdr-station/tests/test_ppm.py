"""Tests for sdr.ppm helpers."""

from __future__ import annotations

import unittest

from sdr.ppm import frequency_error_ppm, mhz_to_hz, suggested_correction_ppm


class PpmTests(unittest.TestCase):
    def test_plus_50_ppm_at_100_mhz(self) -> None:
        expected = mhz_to_hz(100.0)
        measured = mhz_to_hz(100.005)
        self.assertAlmostEqual(frequency_error_ppm(expected, measured), 50.0, places=9)

    def test_suggested_correction_negates_error(self) -> None:
        expected = mhz_to_hz(100.0)
        measured = mhz_to_hz(100.005)
        error = frequency_error_ppm(expected, measured)
        correction = suggested_correction_ppm(expected, measured)
        self.assertAlmostEqual(correction, -error, places=12)
        self.assertAlmostEqual(correction, -50.0, places=9)

    def test_zero_error(self) -> None:
        hz = mhz_to_hz(98.5)
        self.assertEqual(frequency_error_ppm(hz, hz), 0.0)
        self.assertEqual(suggested_correction_ppm(hz, hz), 0.0)

    def test_rejects_zero_expected(self) -> None:
        with self.assertRaises(ValueError):
            frequency_error_ppm(0.0, 1.0)

    def test_mhz_to_hz(self) -> None:
        self.assertEqual(mhz_to_hz(1.0), 1_000_000.0)


if __name__ == "__main__":
    unittest.main()

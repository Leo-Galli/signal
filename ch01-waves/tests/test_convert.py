"""Tests for waves.convert helpers."""

from __future__ import annotations

import math
import unittest

from waves.convert import (
    SPEED_OF_LIGHT_M_S,
    dbm_to_mw,
    mhz_to_wavelength_m,
    mw_to_dbm,
    wavelength_m_to_mhz,
)


class ConvertTests(unittest.TestCase):
    def test_100_mhz_wavelength_near_3m(self) -> None:
        # lambda = c / f; 100 MHz -> 2.99792458 m
        wavelength = mhz_to_wavelength_m(100.0)
        self.assertAlmostEqual(wavelength, SPEED_OF_LIGHT_M_S / 1e8, places=9)

    def test_round_trip_frequency(self) -> None:
        mhz = 433.0
        back = wavelength_m_to_mhz(mhz_to_wavelength_m(mhz))
        self.assertAlmostEqual(back, mhz, places=9)

    def test_0_dbm_is_1_mw(self) -> None:
        self.assertAlmostEqual(mw_to_dbm(1.0), 0.0, places=12)
        self.assertAlmostEqual(dbm_to_mw(0.0), 1.0, places=12)

    def test_10_mw_is_10_dbm(self) -> None:
        self.assertAlmostEqual(mw_to_dbm(10.0), 10.0, places=12)
        self.assertAlmostEqual(dbm_to_mw(10.0), 10.0, places=12)

    def test_1_w_is_30_dbm(self) -> None:
        self.assertAlmostEqual(mw_to_dbm(1000.0), 30.0, places=12)

    def test_rejects_non_positive(self) -> None:
        with self.assertRaises(ValueError):
            mhz_to_wavelength_m(0.0)
        with self.assertRaises(ValueError):
            mw_to_dbm(-1.0)

    def test_dbm_round_trip(self) -> None:
        for mw in (0.001, 0.1, 1.0, 25.0, 1000.0):
            self.assertTrue(math.isclose(dbm_to_mw(mw_to_dbm(mw)), mw, rel_tol=1e-12))


if __name__ == "__main__":
    unittest.main()

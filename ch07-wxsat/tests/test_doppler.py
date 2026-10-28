"""Tests for wxsat.doppler helpers."""

from __future__ import annotations

import unittest

from wxsat.doppler import (
    SPEED_OF_LIGHT_MPS,
    doppler_shift_hz,
    format_doppler,
    observed_frequency_hz,
)


class DopplerTests(unittest.TestCase):
    def test_known_shift(self) -> None:
        # 137.1 MHz with 1000 m/s approach.
        carrier = 137_100_000.0
        shift = doppler_shift_hz(carrier, 1000.0)
        expected = carrier * 1000.0 / SPEED_OF_LIGHT_MPS
        self.assertAlmostEqual(shift, expected, places=6)
        self.assertAlmostEqual(
            observed_frequency_hz(carrier, 1000.0),
            carrier + expected,
            places=6,
        )

    def test_receding_is_negative(self) -> None:
        shift = doppler_shift_hz(137_100_000.0, -1000.0)
        self.assertLess(shift, 0)

    def test_rejects_non_positive_carrier(self) -> None:
        with self.assertRaises(ValueError):
            doppler_shift_hz(0, 10)
        with self.assertRaises(ValueError):
            doppler_shift_hz(-1, 10)

    def test_format(self) -> None:
        text = format_doppler(137_100_000.0, 1000.0)
        self.assertIn("carrier_hz=137100000.0", text)
        self.assertIn("v_radial_mps=1000.0", text)
        self.assertIn("delta_hz=", text)


if __name__ == "__main__":
    unittest.main()

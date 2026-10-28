"""Tests for gnuradio.sample_rates helpers."""

from __future__ import annotations

import unittest

from gnuradio.sample_rates import (
    audio_rate_hz,
    decimation_ok,
    describe_chain,
    nyquist_ok,
    throttle_period_s,
)


class SampleRateTests(unittest.TestCase):
    def test_audio_rate_from_quad_and_decim(self) -> None:
        self.assertAlmostEqual(audio_rate_hz(240_000.0, 5), 48_000.0)

    def test_audio_rate_rejects_bad_inputs(self) -> None:
        with self.assertRaises(ValueError):
            audio_rate_hz(0.0, 5)
        with self.assertRaises(ValueError):
            audio_rate_hz(240_000.0, 0)

    def test_decimation_ok(self) -> None:
        self.assertTrue(decimation_ok(2_400_000.0, 240_000.0, 10))
        self.assertFalse(decimation_ok(2_400_000.0, 200_000.0, 10))

    def test_nyquist_ok(self) -> None:
        self.assertTrue(nyquist_ok(240_000.0, 75_000.0))
        self.assertFalse(nyquist_ok(100_000.0, 75_000.0))

    def test_throttle_period(self) -> None:
        self.assertAlmostEqual(throttle_period_s(2_400_000.0), 1.0 / 2_400_000.0)

    def test_describe_chain_default_book_numbers(self) -> None:
        chain = describe_chain(2_400_000.0, 10, 5)
        self.assertAlmostEqual(chain["quadrature_rate_hz"], 240_000.0)
        self.assertAlmostEqual(chain["audio_rate_hz"], 48_000.0)


if __name__ == "__main__":
    unittest.main()

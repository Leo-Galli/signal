"""Tests for Morse timing helpers."""

from __future__ import annotations

import unittest

from morse.timing import (
    farnsworth_gap_units,
    timing_report,
    unit_seconds,
    validate_timing_params,
)


class TimingTests(unittest.TestCase):
    def test_paris_unit_at_20_wpm(self) -> None:
        self.assertAlmostEqual(unit_seconds(20), 0.06)

    def test_unit_rejects_non_positive(self) -> None:
        with self.assertRaises(ValueError):
            unit_seconds(0)

    def test_equal_speeds_standard_gaps(self) -> None:
        ic, iw = farnsworth_gap_units(20, 20)
        self.assertAlmostEqual(ic, 3.0)
        self.assertAlmostEqual(iw, 7.0)

    def test_farnsworth_stretches_gaps(self) -> None:
        ic, iw = farnsworth_gap_units(20, 10)
        self.assertGreater(ic, 3.0)
        self.assertGreater(iw, 7.0)
        self.assertAlmostEqual(iw / ic, 7.0 / 3.0, places=6)

    def test_effective_faster_than_character_rejected(self) -> None:
        with self.assertRaises(ValueError):
            farnsworth_gap_units(10, 20)

    def test_timing_report_keys(self) -> None:
        report = timing_report(20, 10)
        self.assertIn("dot_seconds", report)
        self.assertIn("inter_character_gap_seconds", report)

    def test_validate_timing_params(self) -> None:
        self.assertEqual(
            validate_timing_params({"character_wpm": 20, "effective_wpm": 10}),
            [],
        )
        self.assertEqual(
            validate_timing_params({"character_wpm": 10, "effective_wpm": 20}),
            ["effective_wpm"],
        )


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

from keyer.dot_timing import average_dit_ms, measure_dot_length
from keyer.timing import unit_ms_from_wpm

ROOT = Path(__file__).resolve().parents[1]


class DotTimingTests(unittest.TestCase):
    def test_average_dit_ignores_dahs(self) -> None:
        # K at 20 WPM: 180, 60, 180 -- dit average should be 60.
        avg = average_dit_ms([180, 60, 180])
        self.assertAlmostEqual(avg, 60.0)

    def test_measure_sample_events(self) -> None:
        payload = json.loads(
            (ROOT / "data" / "sample_key_events.json").read_text(encoding="utf-8")
        )
        result = measure_dot_length(payload["events"], wpm_hint=20)
        self.assertEqual(result["sample_count"], 3)
        self.assertAlmostEqual(result["average_dit_ms"], 60.0)
        self.assertEqual(result["expected_unit_ms"], unit_ms_from_wpm(20))
        self.assertAlmostEqual(result["error_ms"], 0.0)

    def test_empty_marks_raise(self) -> None:
        with self.assertRaises(ValueError):
            measure_dot_length([{"kind": "space", "duration_ms": 60}])


if __name__ == "__main__":
    unittest.main()

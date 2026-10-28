import json
import tempfile
import unittest
from pathlib import Path

from range.plot_rssi import plot_rssi_distance, rssi_distance_series

ROOT = Path(__file__).resolve().parents[1]


class TestPlot(unittest.TestCase):
    def test_series_skips_blanks(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_results_fixture.json").read_text(encoding="utf-8")
        )
        series, skipped = rssi_distance_series(doc)
        self.assertEqual(len(series), 4)
        self.assertEqual(skipped, 1)
        self.assertEqual(series[0][0], 10.0)

    def test_blank_template_all_skipped(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "blank_results.json").read_text(encoding="utf-8")
        )
        series, skipped = rssi_distance_series(doc)
        self.assertEqual(series, [])
        self.assertEqual(skipped, 5)

    def test_plot_writes_png(self) -> None:
        doc = json.loads(
            (ROOT / "data" / "sample_results_fixture.json").read_text(encoding="utf-8")
        )
        series, _ = rssi_distance_series(doc)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.png"
            plot_rssi_distance(series, str(out))
            self.assertTrue(out.is_file())
            self.assertGreater(out.stat().st_size, 100)

    def test_plot_requires_two_points(self) -> None:
        with self.assertRaises(ValueError):
            plot_rssi_distance([(10.0, -70.0)], "unused.png")


if __name__ == "__main__":
    unittest.main()

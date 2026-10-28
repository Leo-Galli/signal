"""Tests for plot_relative_strength without requiring a live SDR."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "plot_relative_strength.py"
SAMPLE = ROOT / "data" / "sample_fm_scan.csv"


def _load_tool():
    spec = importlib.util.spec_from_file_location("plot_relative_strength", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PlotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = _load_tool()

    def test_sample_loads_and_peaks(self) -> None:
        freqs, levels = self.tool.load_scan(SAMPLE)
        self.assertGreaterEqual(len(freqs), 10)
        stats = self.tool.summarize(freqs, levels)
        self.assertEqual(stats["peak_frequency_mhz"], 99.0)
        self.assertEqual(stats["peak_relative_db"], -34.0)

    def test_main_prints_summary(self) -> None:
        code = self.tool.main([str(SAMPLE)])
        self.assertEqual(code, 0)

    def test_main_writes_png_when_matplotlib_present(self) -> None:
        try:
            import matplotlib  # noqa: F401
        except ImportError:
            self.skipTest("matplotlib not installed")
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "scan.png"
            code = self.tool.main([str(SAMPLE), "--out", str(out)])
            self.assertEqual(code, 0)
            self.assertTrue(out.is_file())
            self.assertGreater(out.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()

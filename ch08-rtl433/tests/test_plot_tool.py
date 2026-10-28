"""CLI tests for plot_temperature (summary path; optional PNG)."""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.plot_temperature import main

ROOT = Path(__file__).resolve().parents[1]
SENSOR = ROOT / "data" / "sample_sensor_log.json"


class PlotToolTests(unittest.TestCase):
    def test_summary(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main([str(SENSOR), "--id", "1001"])
        self.assertEqual(code, 0)
        self.assertIn("mean_c=", buf.getvalue())

    def test_png(self) -> None:
        try:
            import matplotlib  # noqa: F401
        except ImportError:
            self.skipTest("matplotlib not installed")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "temp.png"
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = main([str(SENSOR), "--id", "1001", "--out", str(out)])
            self.assertEqual(code, 0)
            self.assertTrue(out.is_file())
            self.assertGreater(out.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()

"""CLI smoke tests for Chapter 9 tools."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.check_sample_rates import main as rates_main
from tools.validate_grc import main as grc_main
from tools.validate_session_notes import main as notes_main

ROOT = Path(__file__).resolve().parents[1]


class ToolSmokeTests(unittest.TestCase):
    def test_validate_live_grc_cli(self) -> None:
        path = ROOT / "flowgraphs" / "wbfm_rtl_receive.grc"
        self.assertEqual(grc_main([str(path), "--kind", "live"]), 0)

    def test_validate_file_grc_cli(self) -> None:
        path = ROOT / "flowgraphs" / "wbfm_file_source.grc"
        self.assertEqual(grc_main([str(path), "--kind", "file"]), 0)

    def test_check_sample_rates_cli(self) -> None:
        self.assertEqual(
            rates_main(
                [
                    "--rf-rate",
                    "2400000",
                    "--channel-decim",
                    "10",
                    "--audio-decim",
                    "5",
                ]
            ),
            0,
        )

    def test_validate_session_notes_cli(self) -> None:
        path = ROOT / "data" / "sample_session_notes.json"
        self.assertEqual(notes_main([str(path), "--kind", "session"]), 0)

    def test_validate_block_versions_cli(self) -> None:
        path = ROOT / "data" / "sample_block_versions.json"
        self.assertEqual(notes_main([str(path), "--kind", "blocks"]), 0)


if __name__ == "__main__":
    unittest.main()

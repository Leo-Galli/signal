"""Tests for gnuradio.grc_parse against checked-in flowgraphs."""

from __future__ import annotations

import unittest
from pathlib import Path

from gnuradio.grc_parse import (
    list_block_ids,
    missing_file_path_blocks,
    missing_live_blocks,
    validate_file_source_grc,
    validate_live_grc,
)

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "flowgraphs" / "wbfm_rtl_receive.grc"
FILE_SRC = ROOT / "flowgraphs" / "wbfm_file_source.grc"


class GrcParseTests(unittest.TestCase):
    def test_live_grc_present_and_valid(self) -> None:
        self.assertTrue(LIVE.is_file())
        self.assertEqual(validate_live_grc(LIVE), [])

    def test_file_source_grc_present_and_valid(self) -> None:
        self.assertTrue(FILE_SRC.is_file())
        self.assertEqual(validate_file_source_grc(FILE_SRC), [])

    def test_live_has_required_ids(self) -> None:
        text = LIVE.read_text(encoding="utf-8")
        self.assertEqual(missing_live_blocks(text), [])
        ids = set(list_block_ids(text))
        self.assertIn("rtlsdr_source", ids)
        self.assertIn("analog_wfm_rcv", ids)

    def test_file_source_has_throttle_and_sink_block(self) -> None:
        text = FILE_SRC.read_text(encoding="utf-8")
        self.assertEqual(missing_file_path_blocks(text), [])
        ids = set(list_block_ids(text))
        self.assertIn("blocks_throttle", ids)
        self.assertIn("blocks_file_sink", ids)

    def test_missing_file(self) -> None:
        self.assertEqual(validate_live_grc(ROOT / "nope.grc"), ["missing_file"])


if __name__ == "__main__":
    unittest.main()

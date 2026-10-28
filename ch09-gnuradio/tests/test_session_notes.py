"""Tests for gnuradio.session_notes."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from gnuradio.session_notes import validate_block_versions, validate_session_notes

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SESSION = ROOT / "data" / "sample_session_notes.json"
SAMPLE_BLOCKS = ROOT / "data" / "sample_block_versions.json"


class SessionNotesTests(unittest.TestCase):
    def test_sample_session_ok(self) -> None:
        doc = json.loads(SAMPLE_SESSION.read_text(encoding="utf-8"))
        self.assertEqual(validate_session_notes(doc), [])

    def test_sample_blocks_ok(self) -> None:
        doc = json.loads(SAMPLE_BLOCKS.read_text(encoding="utf-8"))
        self.assertEqual(validate_block_versions(doc), [])

    def test_missing_field(self) -> None:
        doc = json.loads(SAMPLE_SESSION.read_text(encoding="utf-8"))
        del doc["audio_rate_hz"]
        self.assertIn("audio_rate_hz", validate_session_notes(doc))

    def test_non_positive_rate(self) -> None:
        doc = json.loads(SAMPLE_SESSION.read_text(encoding="utf-8"))
        doc["sample_rate_hz"] = 0
        self.assertEqual(validate_session_notes(doc), ["sample_rate_hz"])

    def test_empty_blocks(self) -> None:
        self.assertEqual(
            validate_block_versions({"gnuradio_version": "3.10", "blocks": []}),
            ["blocks"],
        )


if __name__ == "__main__":
    unittest.main()

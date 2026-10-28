"""CLI smoke tests for Chapter 11 tools."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.decode_wav import main as decode_main
from tools.encode_wav import main as encode_main
from tools.fuzz_timing import main as fuzz_main
from tools.measure_accuracy import main as accuracy_main

ROOT = Path(__file__).resolve().parents[1]


class ToolSmokeTests(unittest.TestCase):
    def test_encode_decode_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "out.wav"
            self.assertEqual(
                encode_main(["HELLO", "-o", str(wav), "--wpm", "20"]),
                0,
            )
            self.assertEqual(decode_main([str(wav), "--wpm-hint", "20"]), 0)

    def test_fuzz_cli(self) -> None:
        self.assertEqual(
            fuzz_main(["PARIS", "--wpm", "20", "--scales", "0.9,1.0,1.1"]),
            0,
        )

    def test_measure_accuracy_cli(self) -> None:
        corpus = ROOT / "data" / "sample_corpus.json"
        self.assertEqual(
            accuracy_main(["--corpus", str(corpus), "--wpm", "20", "--min-accuracy", "1.0"]),
            0,
        )


if __name__ == "__main__":
    unittest.main()

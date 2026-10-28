"""Timing fuzz and corpus accuracy tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from morse.audio import synthesize_wav
from morse.corpus import DEFAULT_CORPUS, score_accuracy, validate_corpus
from morse.decode import decode_pcm

ROOT = Path(__file__).resolve().parents[1]


class FuzzAndCorpusTests(unittest.TestCase):
    def test_timing_fuzz_recovers_phrase(self) -> None:
        text = "PARIS HELLO"
        for scale in (0.9, 1.0, 1.1):
            pcm, rate = synthesize_wav(text, wpm=20, timing_scale=scale)
            decoded = decode_pcm(pcm, sample_rate=rate, wpm_hint=20.0 / scale)
            score = score_accuracy(text, decoded)
            self.assertEqual(
                score["accuracy"],
                1.0,
                msg=f"scale={scale} decoded={decoded!r}",
            )

    def test_default_corpus_perfect(self) -> None:
        for phrase in DEFAULT_CORPUS:
            text = phrase["text"]
            pcm, rate = synthesize_wav(text, wpm=20)
            decoded = decode_pcm(pcm, sample_rate=rate, wpm_hint=20)
            score = score_accuracy(text, decoded)
            self.assertEqual(
                score["accuracy"],
                1.0,
                msg=f"id={phrase['id']} decoded={decoded!r}",
            )

    def test_sample_corpus_json(self) -> None:
        path = ROOT / "data" / "sample_corpus.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(validate_corpus(doc), [])


if __name__ == "__main__":
    unittest.main()

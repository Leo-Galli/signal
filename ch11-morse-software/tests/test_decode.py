"""Encode/decode round-trip tests (noise-free)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from morse.audio import synthesize_wav, write_wav
from morse.corpus import normalize_for_compare, score_accuracy
from morse.decode import decode_pcm, decode_wav_file


class DecodeTests(unittest.TestCase):
    def test_round_trip_hello(self) -> None:
        text = "HELLO WORLD"
        pcm, rate = synthesize_wav(text, wpm=20)
        decoded = decode_pcm(pcm, sample_rate=rate, wpm_hint=20)
        self.assertEqual(normalize_for_compare(decoded), normalize_for_compare(text))

    def test_round_trip_digits(self) -> None:
        text = "DE 1A2B3C"
        pcm, rate = synthesize_wav(text, wpm=18)
        decoded = decode_pcm(pcm, sample_rate=rate, wpm_hint=18)
        self.assertEqual(normalize_for_compare(decoded), normalize_for_compare(text))

    def test_round_trip_prosigns(self) -> None:
        text = "CQ TEST <AR> <SK>"
        pcm, rate = synthesize_wav(text, wpm=20)
        decoded = decode_pcm(pcm, sample_rate=rate, wpm_hint=20)
        self.assertEqual(normalize_for_compare(decoded), normalize_for_compare(text))

    def test_wav_file_round_trip(self) -> None:
        text = "PARIS"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paris.wav"
            pcm, rate = synthesize_wav(text, wpm=20)
            write_wav(path, pcm, sample_rate=rate)
            decoded = decode_wav_file(path, wpm_hint=20)
        self.assertEqual(normalize_for_compare(decoded), text)

    def test_estimate_without_hint(self) -> None:
        text = "SOS"
        # Letter S O S with normal gaps -- not the prosign.
        pcm, rate = synthesize_wav(text, wpm=20, include_prosigns=False)
        decoded = decode_pcm(pcm, sample_rate=rate, include_prosigns=False)
        self.assertEqual(normalize_for_compare(decoded), text)

    def test_score_accuracy_perfect(self) -> None:
        score = score_accuracy("HI", "hi")
        self.assertEqual(score["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()

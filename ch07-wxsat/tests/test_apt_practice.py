"""Tests for practice APT encode/decode."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from wxsat.apt_practice import (
    IMAGE_WIDTH,
    encode_decode_roundtrip,
    read_wav_frame,
    render_frame,
    write_png,
    write_wav,
)


class AptPracticeTests(unittest.TestCase):
    def test_render_size(self) -> None:
        frame = render_frame(lines=16)
        self.assertEqual(len(frame), 16)
        self.assertEqual(len(frame[0]), IMAGE_WIDTH)

    def test_roundtrip_writes_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wav = root / "p.wav"
            png = root / "p.png"
            encode_decode_roundtrip(wav, png, lines=16)
            self.assertTrue(wav.is_file())
            self.assertTrue(png.is_file())
            self.assertGreater(wav.stat().st_size, 100)
            self.assertGreater(png.stat().st_size, 100)
            decoded = read_wav_frame(wav, lines=16)
            self.assertEqual(len(decoded), 16)
            self.assertEqual(len(decoded[0]), IMAGE_WIDTH)

    def test_png_header(self) -> None:
        frame = render_frame(lines=8)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.png"
            write_png(path, frame)
            data = path.read_bytes()
            self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_rejects_zero_lines(self) -> None:
        with self.assertRaises(ValueError):
            render_frame(lines=0)
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "bad.wav"
            write_wav(wav, frame=render_frame(lines=4))
            with self.assertRaises(ValueError):
                read_wav_frame(wav, lines=0)


if __name__ == "__main__":
    unittest.main()

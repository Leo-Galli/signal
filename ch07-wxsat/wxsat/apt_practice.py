"""Practice APT-like WAV encode/decode for offline labs.

Generates a small mono WAV with sync bars and a grayscale test
pattern, then decodes that known format back to a PNG. This is not
a live NOAA APT capture and must not be labeled as satellite imagery.
NOAA POES APT transmitters were decommissioned in 2025.
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

# Practice format constants (documented; not a claim about flight APT).
SAMPLE_RATE = 4800
LINES_PER_SECOND = 2
LINE_SAMPLES = SAMPLE_RATE // LINES_PER_SECOND  # 2400
SYNC_SAMPLES = 80
IMAGE_WIDTH = LINE_SAMPLES - SYNC_SAMPLES  # 2320
DEFAULT_LINES = 64
CARRIER_HZ = 2400.0


def _pixel_value(line: int, column: int, lines: int, width: int) -> int:
    """Return 0..255 test-pattern brightness for one pixel."""
    x_norm = column / max(width - 1, 1)
    y_norm = line / max(lines - 1, 1)
    gradient = int(255 * x_norm)
    bar = 255 if (line // 8) % 2 == 0 and column < 40 else gradient
    diagonal = int(255 * abs(x_norm - y_norm))
    if column > width - 40:
        return diagonal
    return bar


def render_frame(lines: int = DEFAULT_LINES) -> list[list[int]]:
    """Return a 2-D list of pixel values for the practice frame."""
    if lines <= 0:
        raise ValueError("lines must be positive")
    frame: list[list[int]] = []
    for line in range(lines):
        row = [
            _pixel_value(line, column, lines, IMAGE_WIDTH)
            for column in range(IMAGE_WIDTH)
        ]
        frame.append(row)
    return frame


def _line_samples(pixels: list[int]) -> list[float]:
    """Build one line: sync burst then AM-ish carrier for pixels."""
    samples: list[float] = []
    for index in range(SYNC_SAMPLES):
        # Alternating sync bar in the baseband envelope sense.
        samples.append(0.9 if (index // 4) % 2 == 0 else 0.1)
    for value in pixels:
        samples.append(value / 255.0)
    if len(samples) != LINE_SAMPLES:
        raise RuntimeError("line length mismatch")
    return samples


def frame_to_pcm(frame: list[list[int]]) -> bytes:
    """Modulate practice frame to 16-bit mono PCM at SAMPLE_RATE."""
    pcm = bytearray()
    sample_index = 0
    for row in frame:
        envelope = _line_samples(row)
        for env in envelope:
            t = sample_index / SAMPLE_RATE
            # Carrier amplitude follows envelope (practice AM-on-carrier).
            tone = env * math.sin(2.0 * math.pi * CARRIER_HZ * t)
            clipped = max(-1.0, min(1.0, tone))
            pcm.extend(struct.pack("<h", int(clipped * 30000)))
            sample_index += 1
    return bytes(pcm)


def write_wav(path: Path, frame: list[list[int]] | None = None) -> Path:
    """Write a practice WAV and return the path."""
    if frame is None:
        frame = render_frame()
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = frame_to_pcm(frame)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm)
    return path


def _envelope_from_pcm(pcm: bytes) -> list[float]:
    """Recover a simple abs-envelope from interleaved 16-bit mono PCM."""
    if len(pcm) % 2 != 0:
        raise ValueError("pcm length must be even")
    envelope: list[float] = []
    for offset in range(0, len(pcm), 2):
        sample = struct.unpack_from("<h", pcm, offset)[0]
        envelope.append(abs(sample) / 30000.0)
    return envelope


def decode_envelope_to_frame(
    envelope: list[float],
    lines: int | None = None,
) -> list[list[int]]:
    """Slice envelope into practice lines and map image region to pixels."""
    if len(envelope) < LINE_SAMPLES:
        raise ValueError("envelope too short for one line")
    total_lines = lines if lines is not None else len(envelope) // LINE_SAMPLES
    if total_lines <= 0:
        raise ValueError("lines must be positive")
    needed = total_lines * LINE_SAMPLES
    if len(envelope) < needed:
        raise ValueError("envelope shorter than requested lines")

    frame: list[list[int]] = []
    for line in range(total_lines):
        start = line * LINE_SAMPLES + SYNC_SAMPLES
        end = (line + 1) * LINE_SAMPLES
        row = [
            max(0, min(255, int(round(value * 255))))
            for value in envelope[start:end]
        ]
        frame.append(row)
    return frame


def read_wav_frame(path: Path, lines: int | None = None) -> list[list[int]]:
    """Decode a practice WAV written by write_wav."""
    with wave.open(str(path), "rb") as handle:
        if handle.getnchannels() != 1:
            raise ValueError("practice wav must be mono")
        if handle.getsampwidth() != 2:
            raise ValueError("practice wav must be 16-bit")
        if handle.getframerate() != SAMPLE_RATE:
            raise ValueError("practice wav sample rate mismatch")
        pcm = handle.readframes(handle.getnframes())
    envelope = _envelope_from_pcm(pcm)
    return decode_envelope_to_frame(envelope, lines=lines)


def write_png(path: Path, frame: list[list[int]]) -> Path:
    """Write a minimal 8-bit grayscale PNG without third-party deps."""
    if not frame or not frame[0]:
        raise ValueError("frame must be non-empty")
    height = len(frame)
    width = len(frame[0])
    for row in frame:
        if len(row) != width:
            raise ValueError("ragged frame")

    raw = bytearray()
    for row in frame:
        raw.append(0)  # filter none
        raw.extend(max(0, min(255, int(v))) for v in row)

    import zlib

    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return (
            struct.pack(">I", len(data))
            + body
            + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    png = bytearray()
    png.extend(b"\x89PNG\r\n\x1a\n")
    png.extend(chunk(b"IHDR", ihdr))
    png.extend(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
    png.extend(chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    return path


def encode_decode_roundtrip(
    wav_path: Path,
    png_path: Path,
    lines: int = DEFAULT_LINES,
) -> tuple[Path, Path]:
    """Write practice WAV, decode it, write PNG; return both paths."""
    frame = render_frame(lines=lines)
    write_wav(wav_path, frame=frame)
    decoded = read_wav_frame(wav_path, lines=lines)
    write_png(png_path, decoded)
    return wav_path, png_path

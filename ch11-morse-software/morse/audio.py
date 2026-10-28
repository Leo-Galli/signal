"""PCM / WAV tone synthesis for Morse on/off timelines.

Uses only the Python standard library (math + wave + array). No numpy.
"""

from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path
from typing import Sequence

from morse.encode import text_to_on_off


def synthesize_pcm(
    segments: Sequence[tuple[bool, float]],
    *,
    sample_rate: int = 8000,
    tone_hz: float = 700.0,
    amplitude: float = 0.4,
) -> array:
    """Return signed 16-bit mono PCM samples for an on/off timeline."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if amplitude < 0 or amplitude > 1:
        raise ValueError("amplitude must be in [0, 1]")

    samples = array("h")
    peak = int(32767 * amplitude)
    phase = 0.0
    two_pi = 2.0 * math.pi

    for tone_on, duration in segments:
        n = max(0, int(round(duration * sample_rate)))
        for _ in range(n):
            if tone_on:
                value = int(peak * math.sin(phase))
                phase += two_pi * tone_hz / sample_rate
                if phase > two_pi:
                    phase -= two_pi
            else:
                value = 0
                # Keep phase continuous across gaps so tone restarts cleanly.
            samples.append(value)
    return samples


def synthesize_wav(
    text: str,
    *,
    wpm: float = 20.0,
    sample_rate: int = 8000,
    tone_hz: float = 700.0,
    timing_scale: float = 1.0,
    include_prosigns: bool = True,
    amplitude: float = 0.4,
) -> tuple[array, int]:
    """Encode text and return (pcm_samples, sample_rate)."""
    segments = text_to_on_off(
        text,
        wpm=wpm,
        timing_scale=timing_scale,
        include_prosigns=include_prosigns,
    )
    # Small leading/trailing silence helps envelope decoders find edges.
    unit_pad = (False, 1.2 / wpm * 7 * timing_scale)
    padded = [unit_pad, *segments, unit_pad]
    pcm = synthesize_pcm(
        padded,
        sample_rate=sample_rate,
        tone_hz=tone_hz,
        amplitude=amplitude,
    )
    return pcm, sample_rate


def write_wav(
    path: Path | str,
    pcm: array,
    *,
    sample_rate: int = 8000,
) -> None:
    """Write mono 16-bit PCM to a WAV file."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def read_wav(path: Path | str) -> tuple[array, int]:
    """Read a mono 16-bit WAV into (pcm_samples, sample_rate)."""
    with wave.open(str(path), "rb") as handle:
        if handle.getnchannels() != 1:
            raise ValueError("only mono WAV is supported")
        if handle.getsampwidth() != 2:
            raise ValueError("only 16-bit WAV is supported")
        sample_rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    pcm = array("h")
    pcm.frombytes(frames)
    return pcm, sample_rate

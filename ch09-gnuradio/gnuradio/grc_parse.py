"""Lightweight parser checks for a checked-in GNU Radio Companion .grc file.

GNU Radio Companion 3.8+ saves flowgraphs as YAML. This module does not run
GNU Radio. It only confirms the companion .grc still names the blocks the
book expects for the minimal WBFM receive path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REQUIRED_BLOCK_IDS = (
    "options",
    "variable",
    "rtlsdr_source",
    "low_pass_filter",
    "analog_wfm_rcv",
    "audio_sink",
    "blocks_throttle",
    "blocks_file_source",
    "blocks_file_sink",
)

# Blocks required in the live RTL receive graph (not the file-source demo).
LIVE_REQUIRED = (
    "rtlsdr_source",
    "low_pass_filter",
    "analog_wfm_rcv",
    "audio_sink",
)

FILE_PATH_REQUIRED = (
    "blocks_file_source",
    "blocks_throttle",
    "low_pass_filter",
    "analog_wfm_rcv",
    "audio_sink",
)


def _collect_ids(text: str) -> set[str]:
    """Collect block id: values from a YAML .grc without requiring PyYAML."""
    ids: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("id:"):
            value = line[3:].strip().strip("'\"")
            if value:
                ids.add(value)
    return ids


def load_grc_text(path: Path) -> str:
    """Read a .grc file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def list_block_ids(text: str) -> list[str]:
    """Return sorted unique block ids found in .grc text."""
    return sorted(_collect_ids(text))


def missing_live_blocks(text: str) -> list[str]:
    """Return LIVE_REQUIRED ids not present in the .grc text."""
    found = _collect_ids(text)
    return [name for name in LIVE_REQUIRED if name not in found]


def missing_file_path_blocks(text: str) -> list[str]:
    """Return FILE_PATH_REQUIRED ids not present in the file-source .grc."""
    found = _collect_ids(text)
    return [name for name in FILE_PATH_REQUIRED if name not in found]


def validate_live_grc(path: Path) -> list[str]:
    """Return problem labels for the live WBFM RTL .grc."""
    if not path.is_file():
        return ["missing_file"]
    text = load_grc_text(path)
    if "wbfm" not in text.lower() and "WBFM" not in text:
        # Title / id should mention WBFM or wbfm.
        if "wbfm_rtl_receive" not in text:
            return ["title_or_id"]
    missing = missing_live_blocks(text)
    if missing:
        return [f"missing:{name}" for name in missing]
    return []


def validate_file_source_grc(path: Path) -> list[str]:
    """Return problem labels for the file-source practice .grc."""
    if not path.is_file():
        return ["missing_file"]
    text = load_grc_text(path)
    missing = missing_file_path_blocks(text)
    if missing:
        return [f"missing:{name}" for name in missing]
    return []


def summarize_grc(path: Path) -> dict[str, Any]:
    """Return a small summary dict for CLI / notes."""
    text = load_grc_text(path)
    ids = list_block_ids(text)
    return {
        "path": str(path),
        "block_id_count": len(ids),
        "block_ids": ids,
    }

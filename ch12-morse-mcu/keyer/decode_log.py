"""Validate serial decode logs captured from the MCU."""

from __future__ import annotations

from typing import Any


class DecodeLogError(ValueError):
    """Raised when a decode log fails validation."""


_REQUIRED = ("session_id", "board", "wpm", "decoded_text", "practice_only")


def validate_decode_log(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate a decode-log JSON object and return a normalized summary."""
    if not isinstance(payload, dict):
        raise DecodeLogError("payload must be an object")

    missing = [key for key in _REQUIRED if key not in payload]
    if missing:
        raise DecodeLogError(f"missing keys: {', '.join(missing)}")

    session_id = payload["session_id"]
    if not isinstance(session_id, str) or not session_id.strip():
        raise DecodeLogError("session_id must be a non-empty string")

    board = payload["board"]
    if not isinstance(board, str) or not board.strip():
        raise DecodeLogError("board must be a non-empty string")

    wpm = payload["wpm"]
    if not isinstance(wpm, int) or isinstance(wpm, bool) or wpm < 5 or wpm > 40:
        raise DecodeLogError("wpm must be an int from 5 to 40")

    decoded_text = payload["decoded_text"]
    if not isinstance(decoded_text, str):
        raise DecodeLogError("decoded_text must be a string")
    if not decoded_text.strip():
        raise DecodeLogError("decoded_text must not be blank")

    practice_only = payload["practice_only"]
    if practice_only is not True:
        raise DecodeLogError("practice_only must be true (no RF claims in this log)")

    notes = payload.get("notes", "")
    if notes is not None and not isinstance(notes, str):
        raise DecodeLogError("notes must be a string when present")

    return {
        "session_id": session_id.strip(),
        "board": board.strip(),
        "wpm": wpm,
        "decoded_text": decoded_text,
        "char_count": len(decoded_text.replace(" ", "")),
        "practice_only": True,
        "notes": notes or "",
    }

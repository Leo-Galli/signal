"""Decode-rate helpers for ADS-B practice sessions.

Computes messages per minute from reader-recorded counts.
Does not talk to hardware and does not invent traffic.
"""

from __future__ import annotations


def messages_per_minute(message_count: int, duration_minutes: float) -> float:
    """Return message_count / duration_minutes."""
    if duration_minutes <= 0:
        raise ValueError("duration_minutes must be positive")
    if message_count < 0:
        raise ValueError("message_count must be >= 0")
    return message_count / duration_minutes


def format_rate(message_count: int, duration_minutes: float) -> str:
    """Return a one-line decode-rate summary."""
    rate = messages_per_minute(message_count, duration_minutes)
    return (
        f"messages={message_count} minutes={duration_minutes} "
        f"messages_per_minute={rate:.2f}"
    )

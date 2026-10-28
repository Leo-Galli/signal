"""Relative SNR / signal-quality comparison for antenna positions.

Scores are unitless reader-assigned ratings (for example 1-5 from ear
or a host signal meter). This module does not invent decibels from RF
and does not talk to hardware.
"""

from __future__ import annotations


def score_delta(position_a: float, position_b: float) -> float:
    """Return B minus A for two relative quality scores."""
    return position_b - position_a


def prefer_position(
    position_a: float,
    position_b: float,
    label_a: str = "A",
    label_b: str = "B",
) -> str:
    """Return the label of the higher score, or 'tie' if equal."""
    if position_a == position_b:
        return "tie"
    if position_b > position_a:
        return label_b
    return label_a


def summarize_comparison(
    position_a: float,
    position_b: float,
    label_a: str = "A",
    label_b: str = "B",
) -> str:
    """Return a one-line summary of a two-position comparison."""
    delta = score_delta(position_a, position_b)
    winner = prefer_position(position_a, position_b, label_a, label_b)
    if winner == "tie":
        return (
            f"{label_a}={position_a} {label_b}={position_b} "
            f"delta={delta} preferred=tie"
        )
    return (
        f"{label_a}={position_a} {label_b}={position_b} "
        f"delta={delta} preferred={winner}"
    )

"""Software duty-cycle gate mirroring firmware/src/duty_cycle.cpp."""

from __future__ import annotations

from typing import Any


def budget_ms(window_ms: int, duty_cycle_percent: float) -> int:
    if window_ms <= 0:
        raise ValueError("window_ms must be positive")
    if duty_cycle_percent <= 0 or duty_cycle_percent > 100:
        raise ValueError("duty_cycle_percent must be in (0, 100]")
    return int((window_ms * duty_cycle_percent) / 100.0)


class DutyCycleGate:
    """Rolling-window TX gate. Planning aid only -- not legal advice."""

    def __init__(self, duty_cycle_percent: float, window_ms: int = 3_600_000) -> None:
        self.duty_cycle_percent = float(duty_cycle_percent)
        self.window_ms = int(window_ms)
        self.window_start_ms = 0
        self.tx_used_ms = 0

    def _roll(self, now_ms: int) -> None:
        if now_ms - self.window_start_ms >= self.window_ms:
            self.window_start_ms = now_ms
            self.tx_used_ms = 0

    def remaining_ms(self, now_ms: int) -> int:
        self._roll(now_ms)
        budget = budget_ms(self.window_ms, self.duty_cycle_percent)
        if self.tx_used_ms >= budget:
            return 0
        return budget - self.tx_used_ms

    def allow(self, now_ms: int, airtime_ms: int) -> bool:
        if airtime_ms <= 0:
            return False
        return airtime_ms <= self.remaining_ms(now_ms)

    def record(self, now_ms: int, airtime_ms: int) -> None:
        if airtime_ms <= 0:
            return
        self._roll(now_ms)
        self.tx_used_ms += airtime_ms

    def snapshot(self, now_ms: int) -> dict[str, Any]:
        return {
            "duty_cycle_percent": self.duty_cycle_percent,
            "window_ms": self.window_ms,
            "budget_ms": budget_ms(self.window_ms, self.duty_cycle_percent),
            "remaining_ms": self.remaining_ms(now_ms),
            "tx_used_ms": self.tx_used_ms,
            "note": "Planning arithmetic only. Not legal advice.",
        }

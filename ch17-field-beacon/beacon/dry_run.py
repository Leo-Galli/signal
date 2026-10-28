"""Dry-run latch mirroring firmware/src/dry_run.cpp."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DryRunState:
    compile_force: bool = False
    runtime_on: bool = False
    blocked_tx_count: int = 0
    simulated_tx_count: int = 0


def dry_run_init(compile_force: bool = True) -> DryRunState:
    return DryRunState(
        compile_force=compile_force,
        runtime_on=compile_force,
        blocked_tx_count=0,
        simulated_tx_count=0,
    )


def dry_run_active(state: DryRunState) -> bool:
    return state.compile_force or state.runtime_on


def dry_run_set_runtime(state: DryRunState, on: bool) -> None:
    if state.compile_force:
        state.runtime_on = True
        return
    state.runtime_on = on


def note_blocked(state: DryRunState) -> None:
    state.blocked_tx_count += 1


def note_simulated(state: DryRunState) -> None:
    state.simulated_tx_count += 1


def simulate_tx(state: DryRunState, would_key_rf: bool) -> dict[str, object]:
    """Host helper: if dry-run active, never claim RF was keyed."""
    if dry_run_active(state):
        note_blocked(state)
        note_simulated(state)
        return {"keyed_rf": False, "dry_run": True, "simulated": True}
    if not would_key_rf:
        return {"keyed_rf": False, "dry_run": False, "simulated": False}
    return {"keyed_rf": True, "dry_run": False, "simulated": False}

"""Dry-run latch never claims RF when active."""

from __future__ import annotations

import unittest

from beacon.dry_run import dry_run_active, dry_run_init, dry_run_set_runtime, simulate_tx


class TestDryRun(unittest.TestCase):
    def test_compile_force_blocks_rf(self) -> None:
        state = dry_run_init(compile_force=True)
        result = simulate_tx(state, would_key_rf=True)
        self.assertTrue(dry_run_active(state))
        self.assertFalse(result["keyed_rf"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(state.simulated_tx_count, 1)
        self.assertEqual(state.blocked_tx_count, 1)

    def test_compile_force_cannot_clear(self) -> None:
        state = dry_run_init(compile_force=True)
        dry_run_set_runtime(state, False)
        self.assertTrue(dry_run_active(state))

    def test_runtime_only_can_clear(self) -> None:
        state = dry_run_init(compile_force=False)
        dry_run_set_runtime(state, True)
        self.assertTrue(dry_run_active(state))
        dry_run_set_runtime(state, False)
        self.assertFalse(dry_run_active(state))
        live = simulate_tx(state, would_key_rf=True)
        self.assertTrue(live["keyed_rf"])


if __name__ == "__main__":
    unittest.main()

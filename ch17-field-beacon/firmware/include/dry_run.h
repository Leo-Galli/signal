#pragma once

#include <stdbool.h>
#include <stdint.h>

// Dry-run mode never keys RF. Compile-time DRY_RUN=1 forces on at boot;
// runtime latch can also force dry-run (cannot clear a compile-time force).

typedef struct {
  bool compile_force;
  bool runtime_on;
  uint32_t blocked_tx_count;
  uint32_t simulated_tx_count;
} DryRunState;

void dry_run_init(DryRunState *state, bool compile_force);
bool dry_run_active(const DryRunState *state);
void dry_run_set_runtime(DryRunState *state, bool on);
void dry_run_note_blocked(DryRunState *state);
void dry_run_note_simulated(DryRunState *state);

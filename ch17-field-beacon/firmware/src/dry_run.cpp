#include "dry_run.h"

void dry_run_init(DryRunState *state, bool compile_force) {
  if (state == nullptr) {
    return;
  }
  state->compile_force = compile_force;
  state->runtime_on = compile_force;
  state->blocked_tx_count = 0;
  state->simulated_tx_count = 0;
}

bool dry_run_active(const DryRunState *state) {
  if (state == nullptr) {
    return true;
  }
  return state->compile_force || state->runtime_on;
}

void dry_run_set_runtime(DryRunState *state, bool on) {
  if (state == nullptr) {
    return;
  }
  if (state->compile_force) {
    state->runtime_on = true;
    return;
  }
  state->runtime_on = on;
}

void dry_run_note_blocked(DryRunState *state) {
  if (state == nullptr) {
    return;
  }
  state->blocked_tx_count++;
}

void dry_run_note_simulated(DryRunState *state) {
  if (state == nullptr) {
    return;
  }
  state->simulated_tx_count++;
}

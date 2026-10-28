#include "duty_cycle.h"

void duty_cycle_init(DutyCycleGate *gate, float duty_cycle_percent, uint32_t window_ms) {
  if (gate == nullptr) {
    return;
  }
  gate->duty_cycle_percent = duty_cycle_percent;
  gate->window_ms = window_ms == 0 ? 3600000UL : window_ms;
  gate->window_start_ms = 0;
  gate->tx_used_ms = 0;
}

static void maybe_roll_window(DutyCycleGate *gate, uint32_t now_ms) {
  if (now_ms - gate->window_start_ms >= gate->window_ms) {
    gate->window_start_ms = now_ms;
    gate->tx_used_ms = 0;
  }
}

uint32_t duty_cycle_budget_ms(const DutyCycleGate *gate) {
  if (gate == nullptr || gate->duty_cycle_percent <= 0.0f) {
    return 0;
  }
  return static_cast<uint32_t>((gate->window_ms * gate->duty_cycle_percent) / 100.0f);
}

uint32_t duty_cycle_remaining_ms(const DutyCycleGate *gate, uint32_t now_ms) {
  if (gate == nullptr) {
    return 0;
  }
  DutyCycleGate tmp = *gate;
  maybe_roll_window(&tmp, now_ms);
  const uint32_t budget = duty_cycle_budget_ms(&tmp);
  if (tmp.tx_used_ms >= budget) {
    return 0;
  }
  return budget - tmp.tx_used_ms;
}

bool duty_cycle_allow(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms) {
  if (gate == nullptr || airtime_ms == 0) {
    return false;
  }
  maybe_roll_window(gate, now_ms);
  return airtime_ms <= duty_cycle_remaining_ms(gate, now_ms);
}

void duty_cycle_record(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms) {
  if (gate == nullptr || airtime_ms == 0) {
    return;
  }
  maybe_roll_window(gate, now_ms);
  gate->tx_used_ms += airtime_ms;
}

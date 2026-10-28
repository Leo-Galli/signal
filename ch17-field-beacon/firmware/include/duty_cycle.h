#pragma once

#include <stdint.h>

// Software TX gate: rolling-window airtime budget. Planning aid, not a licence.

typedef struct {
  float duty_cycle_percent;
  uint32_t window_ms;
  uint32_t window_start_ms;
  uint32_t tx_used_ms;
} DutyCycleGate;

void duty_cycle_init(DutyCycleGate *gate, float duty_cycle_percent, uint32_t window_ms);
bool duty_cycle_allow(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms);
void duty_cycle_record(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms);
uint32_t duty_cycle_budget_ms(const DutyCycleGate *gate);
uint32_t duty_cycle_remaining_ms(const DutyCycleGate *gate, uint32_t now_ms);

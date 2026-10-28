#pragma once

#include <stdint.h>

// Software TX gate: tracks airtime spent in a rolling window and refuses
// transmits that would exceed duty_cycle_percent. Planning aid, not a licence.

typedef struct {
  float duty_cycle_percent;
  uint32_t window_ms;
  uint32_t window_start_ms;
  uint32_t tx_used_ms;
} DutyCycleGate;

void duty_cycle_init(DutyCycleGate *gate, float duty_cycle_percent, uint32_t window_ms);

// Returns true if airtime_ms fits in the remaining budget at now_ms.
bool duty_cycle_allow(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms);

// Record a completed transmission of airtime_ms starting at now_ms.
void duty_cycle_record(DutyCycleGate *gate, uint32_t now_ms, uint32_t airtime_ms);

uint32_t duty_cycle_budget_ms(const DutyCycleGate *gate);
uint32_t duty_cycle_remaining_ms(const DutyCycleGate *gate, uint32_t now_ms);

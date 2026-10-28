#pragma once

#include <stdint.h>

// Semtech-style packet airtime estimate in milliseconds (teaching mirror of
// ch13-lora-physics). Used to feed the software duty-cycle gate.

uint32_t airtime_est_ms(
  uint8_t sf,
  float bw_hz,
  uint16_t payload_bytes,
  uint8_t cr,
  uint8_t preamble_symbols
);

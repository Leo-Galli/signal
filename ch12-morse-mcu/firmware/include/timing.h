#pragma once

#include <stdint.h>

// PARIS: unit_ms = 1200 / wpm  (same model as ch11-morse-software).
uint16_t unit_ms_from_wpm(uint8_t wpm);
uint8_t clamp_wpm(int value);
uint8_t wpm_from_adc(uint16_t adc_raw, uint16_t adc_max);

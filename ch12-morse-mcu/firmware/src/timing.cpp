#include "timing.h"

uint16_t unit_ms_from_wpm(uint8_t wpm) {
  if (wpm < 5) {
    wpm = 5;
  }
  // Integer form of 1200 / wpm (PARIS unit in milliseconds).
  return static_cast<uint16_t>(1200U / wpm);
}

uint8_t clamp_wpm(int value) {
  if (value < 5) {
    return 5;
  }
  if (value > 40) {
    return 40;
  }
  return static_cast<uint8_t>(value);
}

uint8_t wpm_from_adc(uint16_t adc_raw, uint16_t adc_max) {
  if (adc_max == 0) {
    return 20;
  }
  if (adc_raw > adc_max) {
    adc_raw = adc_max;
  }
  // Map 0..adc_max onto 5..40 WPM inclusive.
  const uint32_t span = 35U;
  const uint32_t mapped = 5U + (static_cast<uint32_t>(adc_raw) * span) / adc_max;
  return clamp_wpm(static_cast<int>(mapped));
}

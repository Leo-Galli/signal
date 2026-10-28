#include "airtime_est.h"

#include <math.h>

uint32_t airtime_est_ms(
  uint8_t sf,
  float bw_hz,
  uint16_t payload_bytes,
  uint8_t cr,
  uint8_t preamble_symbols
) {
  if (sf < 6 || sf > 12 || bw_hz <= 0.0f || cr < 1 || cr > 4) {
    return 0;
  }

  const float t_sym = (static_cast<float>(1u << sf)) / bw_hz;
  const float t_preamble = (static_cast<float>(preamble_symbols) + 4.25f) * t_sym;
  const int de = (sf >= 11) ? 1 : 0;
  const int crc = 1;
  const int h = 0;
  const float numerator =
    8.0f * static_cast<float>(payload_bytes) - 4.0f * static_cast<float>(sf) + 28.0f +
    16.0f * static_cast<float>(crc) - 20.0f * static_cast<float>(h);
  const float denominator = 4.0f * static_cast<float>(sf - 2 * de);
  float n = ceilf(numerator / denominator);
  if (n < 0.0f) {
    n = 0.0f;
  }
  const float payload_symbols = 8.0f + n * static_cast<float>(cr + 4);
  const float t_payload = payload_symbols * t_sym;
  const float ms = (t_preamble + t_payload) * 1000.0f;
  if (ms <= 0.0f) {
    return 0;
  }
  return static_cast<uint32_t>(ms + 0.5f);
}

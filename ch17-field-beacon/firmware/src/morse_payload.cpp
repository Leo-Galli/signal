#include "morse_payload.h"

#include <stdio.h>
#include <string.h>

size_t morse_format_coord(float value, char hemi_pos, char hemi_neg, char *out, size_t out_cap) {
  if (out == nullptr || out_cap < 4) {
    return 0;
  }
  const char hemi = (value >= 0.0f) ? hemi_pos : hemi_neg;
  float abs_v = value;
  if (abs_v < 0.0f) {
    abs_v = -abs_v;
  }
  const int n = snprintf(out, out_cap, "%.5f%c", static_cast<double>(abs_v), hemi);
  if (n <= 0 || static_cast<size_t>(n) >= out_cap) {
    out[0] = '\0';
    return 0;
  }
  return static_cast<size_t>(n);
}

size_t morse_payload_build(const BeaconPayload *payload, char *out, size_t out_cap) {
  if (payload == nullptr || out == nullptr || out_cap < 8) {
    return 0;
  }

  char lat_buf[24];
  char lon_buf[24];
  if (morse_format_coord(payload->lat, 'N', 'S', lat_buf, sizeof(lat_buf)) == 0) {
    return 0;
  }
  if (morse_format_coord(payload->lon, 'E', 'W', lon_buf, sizeof(lon_buf)) == 0) {
    return 0;
  }

  char name[PACKET_NAME_MAX + 1];
  strncpy(name, payload->name, PACKET_NAME_MAX);
  name[PACKET_NAME_MAX] = '\0';
  for (size_t i = 0; name[i] != '\0'; i++) {
    if (name[i] >= 'a' && name[i] <= 'z') {
      name[i] = static_cast<char>(name[i] - 'a' + 'A');
    }
  }
  if (name[0] == '\0') {
    strncpy(name, "NONAME", PACKET_NAME_MAX);
  }

  const int n = snprintf(out, out_cap, "SOS %s %s %s", name, lat_buf, lon_buf);
  if (n <= 0 || static_cast<size_t>(n) >= out_cap || static_cast<size_t>(n) > MORSE_PAYLOAD_MAX) {
    out[0] = '\0';
    return 0;
  }
  return static_cast<size_t>(n);
}

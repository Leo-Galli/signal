#pragma once

#include <stddef.h>
#include <stdint.h>

#include "packet.h"

// Build the CW fallback string: SOS <NAME> <lat> <lon>
// Coordinates use fixed decimal degrees with N/S E/W suffixes (ASCII only).

static const size_t MORSE_PAYLOAD_MAX = 96;

// Returns bytes written excluding NUL, or 0 on error.
size_t morse_payload_build(
  const BeaconPayload *payload,
  char *out,
  size_t out_cap
);

// Format one coordinate component into out (e.g. "45.46427N"). Returns length.
size_t morse_format_coord(float value, char hemi_pos, char hemi_neg, char *out, size_t out_cap);

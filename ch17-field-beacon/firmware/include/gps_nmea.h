#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Minimal NMEA RMC/GGA parser for teaching GPS UART feeds.
// Accepts one sentence at a time (with or without leading '$').

typedef struct {
  bool fix_valid;
  float lat;
  float lon;
  uint32_t sentences_ok;
  uint32_t sentences_bad;
} GpsFix;

void gps_fix_init(GpsFix *fix);
bool gps_nmea_feed_line(GpsFix *fix, const char *line);

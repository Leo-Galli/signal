#include "gps_nmea.h"

#include <stdlib.h>
#include <string.h>

void gps_fix_init(GpsFix *fix) {
  if (fix == nullptr) {
    return;
  }
  fix->fix_valid = false;
  fix->lat = 0.0f;
  fix->lon = 0.0f;
  fix->sentences_ok = 0;
  fix->sentences_bad = 0;
}

static bool checksum_ok(const char *line) {
  if (line == nullptr) {
    return false;
  }
  if (line[0] == '$') {
    line++;
  }
  const char *star = strchr(line, '*');
  if (star == nullptr || star == line) {
    return false;
  }
  uint8_t cs = 0;
  for (const char *p = line; p < star; p++) {
    cs ^= static_cast<uint8_t>(*p);
  }
  char hex[3] = {star[1], star[2], '\0'};
  if (hex[0] == '\0' || hex[1] == '\0') {
    return false;
  }
  const unsigned long want = strtoul(hex, nullptr, 16);
  return want == cs;
}

static float nmea_to_degrees(const char *field, char hemi) {
  if (field == nullptr || field[0] == '\0') {
    return 0.0f;
  }
  const double raw = atof(field);
  const int deg = static_cast<int>(raw / 100.0);
  const double minutes = raw - (static_cast<double>(deg) * 100.0);
  double dec = static_cast<double>(deg) + (minutes / 60.0);
  if (hemi == 'S' || hemi == 'W') {
    dec = -dec;
  }
  return static_cast<float>(dec);
}

static int split_csv(char *s, char **fields, int max_fields) {
  int n = 0;
  if (s == nullptr) {
    return 0;
  }
  fields[n++] = s;
  for (char *p = s; *p != '\0' && n < max_fields; p++) {
    if (*p == ',') {
      *p = '\0';
      fields[n++] = p + 1;
    }
  }
  return n;
}

bool gps_nmea_feed_line(GpsFix *fix, const char *line) {
  if (fix == nullptr || line == nullptr) {
    return false;
  }
  if (!checksum_ok(line)) {
    fix->sentences_bad++;
    return false;
  }

  char buf[120];
  strncpy(buf, line, sizeof(buf) - 1);
  buf[sizeof(buf) - 1] = '\0';
  char *body = buf;
  if (body[0] == '$') {
    body++;
  }
  char *star = strchr(body, '*');
  if (star != nullptr) {
    *star = '\0';
  }

  char *fields[20];
  const int n = split_csv(body, fields, 20);
  if (n < 1) {
    fix->sentences_bad++;
    return false;
  }

  // Talker-agnostic: look for RMC or GGA in the type field (e.g. GPRMC, GNGGA).
  const char *type = fields[0];
  const char *rmc = strstr(type, "RMC");
  const char *gga = strstr(type, "GGA");

  if (rmc != nullptr && rmc[3] == '\0') {
    if (n < 7) {
      fix->sentences_bad++;
      return false;
    }
    const char status = fields[2][0];
    if (status != 'A') {
      fix->fix_valid = false;
      fix->sentences_ok++;
      return true;
    }
    fix->lat = nmea_to_degrees(fields[3], fields[4][0]);
    fix->lon = nmea_to_degrees(fields[5], fields[6][0]);
    fix->fix_valid = true;
    fix->sentences_ok++;
    return true;
  }

  if (gga != nullptr && gga[3] == '\0') {
    if (n < 7) {
      fix->sentences_bad++;
      return false;
    }
    const int quality = atoi(fields[6]);
    if (quality <= 0) {
      fix->fix_valid = false;
      fix->sentences_ok++;
      return true;
    }
    fix->lat = nmea_to_degrees(fields[2], fields[3][0]);
    fix->lon = nmea_to_degrees(fields[4], fields[5][0]);
    fix->fix_valid = true;
    fix->sentences_ok++;
    return true;
  }

  fix->sentences_bad++;
  return false;
}

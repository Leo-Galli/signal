#include "packet.h"

#include <string.h>

uint16_t packet_crc16(const uint8_t *data, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= static_cast<uint16_t>(data[i]) << 8;
    for (uint8_t b = 0; b < 8; b++) {
      if (crc & 0x8000) {
        crc = static_cast<uint16_t>((crc << 1) ^ 0x1021);
      } else {
        crc = static_cast<uint16_t>(crc << 1);
      }
    }
  }
  return crc;
}

static void write_u16(uint8_t *p, uint16_t v) {
  p[0] = static_cast<uint8_t>(v & 0xFF);
  p[1] = static_cast<uint8_t>((v >> 8) & 0xFF);
}

static uint16_t read_u16(const uint8_t *p) {
  return static_cast<uint16_t>(p[0] | (static_cast<uint16_t>(p[1]) << 8));
}

static void write_f32(uint8_t *p, float v) {
  memcpy(p, &v, sizeof(float));
}

static float read_f32(const uint8_t *p) {
  float v = 0.0f;
  memcpy(&v, p, sizeof(float));
  return v;
}

size_t packet_encode(const BeaconPayload *payload, uint8_t *out, size_t out_cap) {
  if (payload == nullptr || out == nullptr) {
    return 0;
  }

  size_t name_len = strnlen(payload->name, PACKET_NAME_MAX);
  const size_t total = 2 + 2 + 1 + name_len + 4 + 4 + 2;
  if (total > out_cap || total > PACKET_MAX_BYTES) {
    return 0;
  }

  size_t o = 0;
  out[o++] = PACKET_MAGIC0;
  out[o++] = PACKET_MAGIC1;
  write_u16(out + o, payload->seq);
  o += 2;
  out[o++] = static_cast<uint8_t>(name_len);
  memcpy(out + o, payload->name, name_len);
  o += name_len;
  write_f32(out + o, payload->lat);
  o += 4;
  write_f32(out + o, payload->lon);
  o += 4;

  const uint16_t crc = packet_crc16(out, o);
  write_u16(out + o, crc);
  o += 2;
  return o;
}

bool packet_decode(const uint8_t *buf, size_t len, BeaconPayload *out) {
  if (buf == nullptr || out == nullptr || len < 2 + 2 + 1 + 4 + 4 + 2) {
    return false;
  }
  if (buf[0] != PACKET_MAGIC0 || buf[1] != PACKET_MAGIC1) {
    return false;
  }

  const uint8_t name_len = buf[4];
  if (name_len > PACKET_NAME_MAX) {
    return false;
  }
  const size_t expected = 2 + 2 + 1 + name_len + 4 + 4 + 2;
  if (len < expected) {
    return false;
  }

  const uint16_t got = read_u16(buf + expected - 2);
  const uint16_t want = packet_crc16(buf, expected - 2);
  if (got != want) {
    return false;
  }

  memset(out, 0, sizeof(*out));
  out->seq = read_u16(buf + 2);
  memcpy(out->name, buf + 5, name_len);
  out->name[name_len] = '\0';
  out->lat = read_f32(buf + 5 + name_len);
  out->lon = read_f32(buf + 5 + name_len + 4);
  return true;
}

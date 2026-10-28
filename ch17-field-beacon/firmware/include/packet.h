#pragma once

#include <stddef.h>
#include <stdint.h>

// Compact teaching payload: name + GPS-style lat/lon + sequence + CRC-16/CCITT.
// Layout (little-endian floats / uint16):
//   magic[2]=0x53 0x31 ('S','1') | seq u16 | name_len u8 | name[0..15] |
//   lat f32 | lon f32 | crc16 u16 over all prior bytes

static const uint8_t PACKET_MAGIC0 = 0x53;
static const uint8_t PACKET_MAGIC1 = 0x31;
static const size_t PACKET_NAME_MAX = 15;
static const size_t PACKET_MAX_BYTES = 2 + 2 + 1 + PACKET_NAME_MAX + 4 + 4 + 2;

typedef struct {
  uint16_t seq;
  char name[PACKET_NAME_MAX + 1];
  float lat;
  float lon;
} BeaconPayload;

uint16_t packet_crc16(const uint8_t *data, size_t len);
size_t packet_encode(const BeaconPayload *payload, uint8_t *out, size_t out_cap);
bool packet_decode(const uint8_t *buf, size_t len, BeaconPayload *out);

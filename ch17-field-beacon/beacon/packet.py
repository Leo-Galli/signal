"""Beacon payload encode/decode mirroring firmware/src/packet.cpp."""

from __future__ import annotations

import struct
from typing import Any

MAGIC = b"S1"
NAME_MAX = 15
MAX_BYTES = 2 + 2 + 1 + NAME_MAX + 4 + 4 + 2


def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def encode(seq: int, name: str, lat: float, lon: float) -> bytes:
    if seq < 0 or seq > 0xFFFF:
        raise ValueError("seq must fit in uint16")
    name_b = name.encode("ascii")
    if len(name_b) > NAME_MAX:
        raise ValueError(f"name longer than {NAME_MAX} bytes")
    body = MAGIC + struct.pack("<H", seq) + bytes([len(name_b)]) + name_b
    body += struct.pack("<ff", float(lat), float(lon))
    return body + struct.pack("<H", crc16_ccitt(body))


def decode(buf: bytes) -> dict[str, Any]:
    if len(buf) < 2 + 2 + 1 + 4 + 4 + 2:
        raise ValueError("buffer too short")
    if buf[0:2] != MAGIC:
        raise ValueError("bad magic")
    name_len = buf[4]
    if name_len > NAME_MAX:
        raise ValueError("name_len too large")
    expected = 2 + 2 + 1 + name_len + 4 + 4 + 2
    if len(buf) < expected:
        raise ValueError("buffer shorter than name_len")
    payload, crc_bytes = buf[: expected - 2], buf[expected - 2 : expected]
    (got,) = struct.unpack("<H", crc_bytes)
    want = crc16_ccitt(payload)
    if got != want:
        raise ValueError(f"CRC mismatch got=0x{got:04x} want=0x{want:04x}")
    seq = struct.unpack("<H", payload[2:4])[0]
    name = payload[5 : 5 + name_len].decode("ascii")
    lat, lon = struct.unpack("<ff", payload[5 + name_len : 5 + name_len + 8])
    return {
        "seq": seq,
        "name": name,
        "lat": lat,
        "lon": lon,
        "bytes": expected,
    }

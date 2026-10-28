"""Minimal NMEA RMC/GGA parser mirroring firmware/src/gps_nmea.cpp."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GpsFix:
    fix_valid: bool = False
    lat: float = 0.0
    lon: float = 0.0
    sentences_ok: int = 0
    sentences_bad: int = 0


def _checksum_ok(line: str) -> bool:
    body = line[1:] if line.startswith("$") else line
    if "*" not in body:
        return False
    payload, hex_cs = body.split("*", 1)
    if len(hex_cs) < 2:
        return False
    cs = 0
    for ch in payload:
        cs ^= ord(ch)
    try:
        want = int(hex_cs[:2], 16)
    except ValueError:
        return False
    return cs == want


def _nmea_to_degrees(field: str, hemi: str) -> float:
    if not field:
        return 0.0
    raw = float(field)
    deg = int(raw / 100.0)
    minutes = raw - (deg * 100.0)
    dec = deg + (minutes / 60.0)
    if hemi in ("S", "W"):
        dec = -dec
    return dec


def feed_line(fix: GpsFix, line: str) -> bool:
    line = line.strip()
    if not _checksum_ok(line):
        fix.sentences_bad += 1
        return False
    body = line[1:] if line.startswith("$") else line
    body = body.split("*", 1)[0]
    fields = body.split(",")
    if not fields:
        fix.sentences_bad += 1
        return False
    type_field = fields[0]
    if type_field.endswith("RMC"):
        if len(fields) < 7:
            fix.sentences_bad += 1
            return False
        if fields[2] != "A":
            fix.fix_valid = False
            fix.sentences_ok += 1
            return True
        fix.lat = _nmea_to_degrees(fields[3], fields[4])
        fix.lon = _nmea_to_degrees(fields[5], fields[6])
        fix.fix_valid = True
        fix.sentences_ok += 1
        return True
    if type_field.endswith("GGA"):
        if len(fields) < 7:
            fix.sentences_bad += 1
            return False
        try:
            quality = int(fields[6] or "0")
        except ValueError:
            quality = 0
        if quality <= 0:
            fix.fix_valid = False
            fix.sentences_ok += 1
            return True
        fix.lat = _nmea_to_degrees(fields[2], fields[3])
        fix.lon = _nmea_to_degrees(fields[4], fields[5])
        fix.fix_valid = True
        fix.sentences_ok += 1
        return True
    fix.sentences_bad += 1
    return False

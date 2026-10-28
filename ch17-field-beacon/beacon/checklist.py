"""Field checklist validator -- required keys, no invented GPS tracks."""

from __future__ import annotations

from typing import Any

REQUIRED_KEYS = (
    "date",
    "operator_name_field",
    "jurisdiction_worksheet_done",
    "antenna_attached",
    "dry_run_verified",
    "power_setting_dBm",
    "duty_cycle_percent",
    "battery_checked",
    "false_distress_acknowledged",
    "signed",
)


def validate_checklist(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["checklist must be an object"]
    for key in REQUIRED_KEYS:
        if key not in doc:
            errors.append(f"missing key: {key}")
    if doc.get("jurisdiction_worksheet_done") is not True:
        errors.append("jurisdiction_worksheet_done must be true")
    if doc.get("antenna_attached") is not True:
        errors.append("antenna_attached must be true before live RF")
    if doc.get("dry_run_verified") is not True:
        errors.append("dry_run_verified must be true")
    if doc.get("false_distress_acknowledged") is not True:
        errors.append("false_distress_acknowledged must be true")
    if doc.get("signed") is not True:
        errors.append("signed must be true")
    if doc.get("invented_gps_track") is True:
        errors.append("invented_gps_track must not be true")
    return errors

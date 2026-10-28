"""Seven-day Morse practice log validation for Chapter 10.

Does not invent accuracy numbers. Validates structure only so the reader can
keep honest WPM and accuracy notes during the hands-on week.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

REQUIRED_META_FIELDS = (
    "trainer_name",
    "trainer_url_or_path",
    "start_date",
    "character_wpm_target",
    "effective_wpm_start",
    "practice_mode",
    "receive_only_ack",
)

REQUIRED_DAY_FIELDS = (
    "day",
    "date",
    "minutes",
    "character_wpm",
    "effective_wpm",
    "accuracy_percent",
    "notes",
)


def missing_fields(doc: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return names of required fields that are missing or blank."""
    missing: list[str] = []
    for name in required:
        value = doc.get(name, "")
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(name)
            continue
        if not isinstance(value, str) and value == "":
            missing.append(name)
    return missing


def _require_number(
    entry: Mapping[str, Any],
    name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> str | None:
    if name not in entry:
        return name
    try:
        value = float(entry[name])
    except (TypeError, ValueError):
        return name
    if minimum is not None and value < minimum:
        return name
    if maximum is not None and value > maximum:
        return name
    return None


def validate_day(entry: Mapping[str, Any], index: int) -> list[str]:
    """Return problem labels for one practice day."""
    prefix = f"days[{index}]"
    problems = missing_fields(entry, REQUIRED_DAY_FIELDS)
    if problems:
        return [f"{prefix}.{name}" for name in problems]

    day_problem = _require_number(entry, "day", minimum=1, maximum=7)
    if day_problem:
        return [f"{prefix}.{day_problem}"]
    if int(float(entry["day"])) != float(entry["day"]):
        return [f"{prefix}.day"]

    for name, minimum, maximum in (
        ("minutes", 1.0, 180.0),
        ("character_wpm", 1.0, 60.0),
        ("effective_wpm", 1.0, 60.0),
        ("accuracy_percent", 0.0, 100.0),
    ):
        problem = _require_number(entry, name, minimum=minimum, maximum=maximum)
        if problem:
            return [f"{prefix}.{problem}"]

    if float(entry["effective_wpm"]) > float(entry["character_wpm"]):
        return [f"{prefix}.effective_wpm"]

    notes = str(entry.get("notes", "")).strip()
    if len(notes) < 3:
        return [f"{prefix}.notes"]

    return []


def validate_practice_log(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels for a seven-day practice log document."""
    problems = missing_fields(doc, REQUIRED_META_FIELDS)
    if problems:
        return problems

    ack = str(doc.get("receive_only_ack", "")).strip().lower()
    if ack not in {"yes", "true", "acknowledged"}:
        return ["receive_only_ack"]

    for name in ("character_wpm_target", "effective_wpm_start"):
        problem = _require_number(doc, name, minimum=1.0, maximum=60.0)
        if problem:
            return [problem]

    if float(doc["effective_wpm_start"]) > float(doc["character_wpm_target"]):
        return ["effective_wpm_start"]

    days = doc.get("days")
    if not isinstance(days, Sequence) or isinstance(days, (str, bytes)):
        return ["days"]
    if len(days) != 7:
        return ["days"]

    seen_days: set[int] = set()
    for index, entry in enumerate(days):
        if not isinstance(entry, Mapping):
            return [f"days[{index}]"]
        day_problems = validate_day(entry, index)
        if day_problems:
            return day_problems
        day_num = int(float(entry["day"]))
        if day_num in seen_days:
            return [f"days[{index}].day"]
        seen_days.add(day_num)

    if seen_days != set(range(1, 8)):
        return ["days"]

    return []

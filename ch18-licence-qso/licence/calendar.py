"""Four-week study calendar validation for Chapter 18.

Does not invent exam dates, fees or pass scores. Reader fills days from
official syllabus / question-pool study only.
"""

from __future__ import annotations

from typing import Any, Mapping

REQUIRED_CALENDAR_FIELDS = (
    "path_chosen",
    "start_date",
    "not_legal_advice_ack",
    "weeks",
)

ALLOWED_PATHS = frozenset({"italy_mimit", "us_fcc", "other"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"

WEEK_COUNT = 4
DAYS_PER_WEEK = 7


def _iso_date_ok(value: Any) -> bool:
    text = str(value).strip() if value is not None else ""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    year, month, day = text.split("-")
    return year.isdigit() and month.isdigit() and day.isdigit()


def validate_calendar(doc: Mapping[str, Any]) -> list[str]:
    """Return problem labels; empty list means OK."""
    problems: list[str] = []
    for name in REQUIRED_CALENDAR_FIELDS:
        if name not in doc or doc.get(name) is None:
            problems.append(name)
    if problems:
        return problems

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    if not _iso_date_ok(doc.get("start_date")):
        return ["start_date"]

    ack = str(doc.get("not_legal_advice_ack", "")).strip()
    if ack != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    weeks = doc.get("weeks")
    if not isinstance(weeks, list) or len(weeks) != WEEK_COUNT:
        return ["weeks"]

    for i, week in enumerate(weeks):
        if not isinstance(week, dict):
            return [f"weeks[{i}]"]
        if not str(week.get("theme", "")).strip():
            return [f"weeks[{i}].theme"]
        days = week.get("days")
        if not isinstance(days, list) or len(days) != DAYS_PER_WEEK:
            return [f"weeks[{i}].days"]
        for j, day in enumerate(days):
            if not isinstance(day, dict):
                return [f"weeks[{i}].days[{j}]"]
            if "minutes" not in day:
                return [f"weeks[{i}].days[{j}].minutes"]
            minutes = day.get("minutes")
            if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes < 0:
                return [f"weeks[{i}].days[{j}].minutes"]
            if not str(day.get("focus", "")).strip() and minutes > 0:
                return [f"weeks[{i}].days[{j}].focus"]
            done = day.get("done")
            if done is not None and not isinstance(done, bool):
                return [f"weeks[{i}].days[{j}].done"]

    return []


def total_planned_minutes(doc: Mapping[str, Any]) -> int:
    """Sum planned minutes across the four weeks."""
    total = 0
    weeks = doc.get("weeks")
    if not isinstance(weeks, list):
        return 0
    for week in weeks:
        if not isinstance(week, dict):
            continue
        days = week.get("days")
        if not isinstance(days, list):
            continue
        for day in days:
            if isinstance(day, dict) and isinstance(day.get("minutes"), int):
                total += int(day["minutes"])
    return total

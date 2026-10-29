"""Practice quiz scoring for Chapter 18.

US path: original companion practice items aligned to Technician topic areas.
Italy path: HAREC-aligned syllabus checklist items (self-rated readiness).

Neither path is an official exam. Not legal advice. Do not treat a score as
authorization to transmit.
"""

from __future__ import annotations

from typing import Any, Mapping

ALLOWED_PATHS = frozenset({"us_fcc", "italy_mimit"})

NOT_LEGAL_ADVICE_ACK = "I understand this worksheet is not legal advice"


def validate_quiz_doc(doc: Mapping[str, Any]) -> list[str]:
    """Validate quiz structure before scoring."""
    if not isinstance(doc, dict):
        return ["root"]

    path = str(doc.get("path_chosen", "")).strip()
    if path not in ALLOWED_PATHS:
        return ["path_chosen"]

    ack = str(doc.get("not_legal_advice_ack", "")).strip()
    if ack != NOT_LEGAL_ADVICE_ACK:
        return ["not_legal_advice_ack"]

    if str(doc.get("disclaimer", "")).strip().lower().find("not an official") < 0:
        return ["disclaimer"]

    items = doc.get("items")
    if not isinstance(items, list) or len(items) < 5:
        return ["items"]

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return [f"items[{i}]"]
        if not str(item.get("id", "")).strip():
            return [f"items[{i}].id"]
        if not str(item.get("prompt", "")).strip():
            return [f"items[{i}].prompt"]
        kind = str(item.get("kind", "")).strip()
        if kind == "mcq":
            choices = item.get("choices")
            if not isinstance(choices, list) or len(choices) < 2:
                return [f"items[{i}].choices"]
            answer = item.get("answer")
            if not isinstance(answer, str) or answer not in choices:
                return [f"items[{i}].answer"]
        elif kind == "checklist":
            if "ready" not in item:
                return [f"items[{i}].ready"]
            if not isinstance(item.get("ready"), bool):
                return [f"items[{i}].ready"]
        else:
            return [f"items[{i}].kind"]

    return []


def score_quiz(doc: Mapping[str, Any], responses: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Score a validated quiz.

    For mcq items, `responses` maps item id -> chosen choice string.
    For checklist items, readiness comes from the quiz document itself.
    """
    problems = validate_quiz_doc(doc)
    if problems:
        return {"ok": False, "problems": problems}

    items = doc["items"]
    path = str(doc["path_chosen"]).strip()
    responses = responses or {}

    correct = 0
    total = 0
    detail: list[dict[str, Any]] = []

    for item in items:
        item_id = str(item["id"])
        kind = str(item["kind"])
        total += 1
        if kind == "mcq":
            chosen = responses.get(item_id, item.get("selected"))
            is_correct = chosen == item["answer"]
            if is_correct:
                correct += 1
            detail.append(
                {
                    "id": item_id,
                    "kind": kind,
                    "correct": bool(is_correct),
                    "chosen": chosen,
                    "answer": item["answer"],
                }
            )
        else:
            ready = bool(item.get("ready"))
            if ready:
                correct += 1
            detail.append(
                {
                    "id": item_id,
                    "kind": kind,
                    "correct": ready,
                    "ready": ready,
                }
            )

    percent = round(100.0 * correct / total, 1) if total else 0.0
    return {
        "ok": True,
        "path_chosen": path,
        "correct": correct,
        "total": total,
        "percent": percent,
        "detail": detail,
        "not_authorization": True,
    }

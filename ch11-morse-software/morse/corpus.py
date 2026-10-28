"""Fixed decode corpus and accuracy scoring for Chapter 11 exercises."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


DEFAULT_CORPUS: list[dict[str, str]] = [
    {"id": "cq", "text": "CQ CQ CQ"},
    {"id": "paris", "text": "PARIS PARIS"},
    {"id": "hello", "text": "HELLO WORLD"},
    {"id": "digits", "text": "DE 1A2B3C"},
    {"id": "test", "text": "TEST 123"},
]


def normalize_for_compare(text: str) -> str:
    """Uppercase, collapse whitespace, strip for fair accuracy compare."""
    return " ".join(text.upper().split())


def score_accuracy(expected: str, actual: str) -> dict[str, float | int | str]:
    """Character-level accuracy after normalization.

    Returns expected_len, matches, accuracy (0..1), and both strings.
    """
    exp = normalize_for_compare(expected)
    act = normalize_for_compare(actual)
    # Pad the shorter side so every expected character is scored.
    n = max(len(exp), len(act), 1)
    exp_p = exp.ljust(n)
    act_p = act.ljust(n)
    matches = sum(1 for a, b in zip(exp_p, act_p) if a == b)
    return {
        "expected": exp,
        "actual": act,
        "expected_len": len(exp),
        "matches": matches,
        "compared_len": n,
        "accuracy": matches / n,
    }


def validate_corpus(doc: Mapping[str, Any]) -> list[str]:
    """Validate a corpus JSON document. Return list of problem field paths."""
    problems: list[str] = []
    if "phrases" not in doc or not isinstance(doc["phrases"], list):
        return ["phrases"]
    phrases: Sequence[Any] = doc["phrases"]
    if not phrases:
        return ["phrases"]
    seen: set[str] = set()
    for idx, item in enumerate(phrases):
        if not isinstance(item, Mapping):
            problems.append(f"phrases[{idx}]")
            continue
        for key in ("id", "text"):
            if key not in item or not isinstance(item[key], str) or not item[key].strip():
                problems.append(f"phrases[{idx}].{key}")
        phrase_id = str(item.get("id", ""))
        if phrase_id in seen:
            problems.append(f"phrases[{idx}].id")
        seen.add(phrase_id)
    return problems

"""Dumb pattern scan for secrets that must not enter git."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

# Teaching placeholders that look like keys but are safe fixtures.
ALLOWLIST_SUBSTRINGS = (
    "YOUR_APP_KEY_HERE",
    "YOUR_NWK_KEY_HERE",
    "00" * 16,
    "AABBCCDDEEFF00112233445566778899",
    "PLACEHOLDER",
)

HEX_32 = re.compile(r"\b[0-9A-Fa-f]{32}\b")
HEX_64 = re.compile(r"\b[0-9A-Fa-f]{64}\b")
PEM = re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----")
ASSIGNMENT = re.compile(
    r"(?i)\b(appkey|nwkkey|appskey|nwkskey|password|api[_-]?key|token)\s*[=:]\s*['\"]?([^\s'\"]+)"
)

SKIP_DIR_NAMES = {
    ".git",
    ".pio",
    "__pycache__",
    ".venv",
    "node_modules",
    ".pytest_cache",
}


def _is_allowlisted(text: str) -> bool:
    upper = text.upper()
    return any(s.upper() in upper for s in ALLOWLIST_SUBSTRINGS)


def scan_text(text: str, *, source: str = "<memory>") -> list[dict[str, Any]]:
    """Return findings for key-shaped patterns in text."""
    findings: list[dict[str, Any]] = []
    if _is_allowlisted(text):
        # Still flag PEM; placeholders rarely include private key blocks.
        if PEM.search(text):
            findings.append(
                {
                    "source": source,
                    "kind": "pem_private_key",
                    "snippet": "-----BEGIN ... PRIVATE KEY-----",
                }
            )
        return findings

    for kind, cre in (("hex32", HEX_32), ("hex64", HEX_64)):
        for match in cre.finditer(text):
            val = match.group(0)
            if _is_allowlisted(val):
                continue
            findings.append(
                {
                    "source": source,
                    "kind": kind,
                    "snippet": val[:8] + "..." + val[-4:],
                }
            )

    if PEM.search(text):
        findings.append(
            {
                "source": source,
                "kind": "pem_private_key",
                "snippet": "-----BEGIN ... PRIVATE KEY-----",
            }
        )

    for match in ASSIGNMENT.finditer(text):
        name, value = match.group(1), match.group(2)
        if _is_allowlisted(value) or value.upper() in {
            "NULL",
            "NONE",
            "TODO",
            "CHANGEME",
            "YOUR_APP_KEY_HERE",
        }:
            continue
        if len(value) < 8:
            continue
        findings.append(
            {
                "source": source,
                "kind": "assignment",
                "snippet": f"{name}=...",
            }
        )

    return findings


def scan_paths(paths: Iterable[Path]) -> list[dict[str, Any]]:
    """Scan files under paths; skip binary-ish and known junk dirs."""
    findings: list[dict[str, Any]] = []
    for root in paths:
        root = Path(root)
        if root.is_file():
            findings.extend(_scan_file(root))
            continue
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".bin", ".elf", ".o"}:
                continue
            findings.extend(_scan_file(path))
    return findings


def _scan_file(path: Path) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return scan_text(text, source=str(path))

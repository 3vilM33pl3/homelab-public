#!/usr/bin/env python3
"""Scan the public repo for forbidden private literals."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IGNORED_PARTS = {".git", ".terraform", "__pycache__"}
IGNORED_RELATIVE_PATHS = {
    Path("config/sanitization-rules.json"),
    Path("tools/check-public-tree.py"),
}


def load_rules(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def scan_tree(root: Path, patterns: list[str]) -> list[str]:
    failures: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".gif", ".pyc"}:
            continue
        relative_path = path.relative_to(root)
        if relative_path in IGNORED_RELATIVE_PATHS:
            continue
        if "tests" in relative_path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in patterns:
            if re.search(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path}: matched forbidden pattern {pattern}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repo root to scan.",
    )
    parser.add_argument(
        "--rules",
        default=Path(__file__).resolve().parents[1] / "config" / "sanitization-rules.json",
        type=Path,
    )
    args = parser.parse_args()

    rules = load_rules(args.rules)
    failures = scan_tree(args.root.resolve(), rules.get("forbidden_patterns", []))
    if failures:
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Copy a curated subset of the private homelab repo into this public repo."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


def load_rules(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def apply_replacements(text: str, replacements: list[dict]) -> str:
    for rule in replacements:
        text = re.sub(rule["pattern"], rule["replacement"], text)
    return text


def export_files(source: Path, dest: Path, rules: dict) -> None:
    for mapping in rules["file_mappings"]:
        src = source / mapping["src"]
        dst = dest / mapping["dest"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        text = apply_replacements(text, rules["replacements"])
        dst.write_text(text, encoding="utf-8")


def remove_generated_files(dest: Path, rules: dict) -> None:
    for mapping in rules["file_mappings"]:
        path = dest / mapping["dest"]
        if path.exists():
            path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument(
        "--dest",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Public repo root. Defaults to the repository containing this script.",
    )
    parser.add_argument(
        "--rules",
        default=Path(__file__).resolve().parents[1] / "config" / "sanitization-rules.json",
        type=Path,
    )
    parser.add_argument(
        "--clean-generated",
        action="store_true",
        help="Remove generated files before exporting.",
    )
    args = parser.parse_args()

    rules = load_rules(args.rules)
    if args.clean_generated:
        remove_generated_files(args.dest, rules)
    export_files(args.source.resolve(), args.dest.resolve(), rules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Copy a curated subset of the private homelab repo into this public repo."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path


def load_rules(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def apply_replacements(text: str, replacements: list[dict]) -> str:
    for rule in replacements:
        text = re.sub(rule["pattern"], rule["replacement"], text, flags=re.MULTILINE)
    return text


def render_mappings(source: Path, dest: Path, rules: dict) -> dict[Path, str]:
    rendered: dict[Path, str] = {}
    for mapping in rules["file_mappings"]:
        src = source / mapping["src"]
        if not src.is_file():
          raise FileNotFoundError(f"Mapped source is missing or unreadable: {src}")
        target = dest / mapping["dest"]
        text = src.read_text(encoding="utf-8")
        rendered[target] = apply_replacements(text, rules["replacements"])
    return rendered


def scan_rendered(rendered: dict[Path, str], rules: dict) -> list[str]:
    failures: list[str] = []
    for path, text in rendered.items():
        for pattern in rules.get("forbidden_patterns", []):
            if re.search(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path}: matched forbidden pattern {pattern}")
    return failures


def print_diff(path: Path, new_text: str) -> bool:
    old_text = path.read_text(encoding="utf-8") if path.exists() else ""
    if old_text == new_text:
        return False
    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile=str(path),
        tofile=str(path),
        lineterm="",
    )
    print("\n".join(diff))
    return True


def write_rendered(rendered: dict[Path, str]) -> None:
    for path, text in rendered.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render outputs without writing files.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print unified diffs for files that would change.",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Validate mapped outputs against forbidden patterns without writing files.",
    )
    args = parser.parse_args()

    rules = load_rules(args.rules)
    rendered = render_mappings(args.source.resolve(), args.dest.resolve(), rules)
    failures = scan_rendered(rendered, rules)
    if failures:
        print("\n".join(failures))
        return 1

    diff_found = False
    if args.diff or args.dry_run:
        for path, text in rendered.items():
            diff_found = print_diff(path, text) or diff_found

    if args.scan_only:
        return 0

    if args.clean_generated and not args.dry_run:
        remove_generated_files(args.dest.resolve(), rules)

    if not args.dry_run:
        write_rendered(rendered)

    if args.dry_run and diff_found:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

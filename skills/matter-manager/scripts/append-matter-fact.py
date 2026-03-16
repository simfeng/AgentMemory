#!/usr/bin/env python3
"""
Append new fact lines to facts.md without reading the file.

Examples:
  append-matter-fact.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --line "- 2026-03-16 10:30: user confirmed the forecast scope"
  append-matter-fact.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --line "- 2026-03-16 10:35: user uploaded a new data file"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append new fact lines to facts.md. This script never reads the file.",
        epilog=(
            "Examples:\n"
            "  append-matter-fact.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --line \"- 2026-03-16 10:30: user confirmed scope\"\n"
            "  append-matter-fact.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --line \"- 2026-03-16 10:35: user sent new data\""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("facts_file", help="Path to facts.md")
    parser.add_argument(
        "--line",
        action="append",
        default=[],
        help="A fact line to append. Can be used more than once.",
    )
    args = parser.parse_args()
    if not args.line and sys.stdin.isatty():
        parser.error("Provide --line or pipe text into stdin.")
    return args


def validate_facts_file(path: Path) -> None:
    if path.name != "facts.md":
        raise SystemExit("Only facts.md can be updated with this script.")


def normalize_lines(lines: list[str]) -> list[str]:
    normalized: list[str] = []
    for line in lines:
        if not line:
            continue
        prepared = line if line.endswith("\n") else f"{line}\n"
        if not prepared.startswith("- "):
            raise SystemExit("Each appended line must start with '- '.")
        normalized.append(prepared)
    return normalized


def main() -> int:
    args = parse_args()
    facts_path = Path(args.facts_file).expanduser()
    validate_facts_file(facts_path)

    input_lines = list(args.line)
    if not sys.stdin.isatty():
        input_lines.extend(sys.stdin.readlines())

    lines_to_append = normalize_lines(input_lines)
    if not lines_to_append:
        return 0
    if not facts_path.exists():
        raise SystemExit("facts.md must already exist before append.")

    with facts_path.open("a", encoding="utf-8") as handle:
        handle.writelines(lines_to_append)

    payload = {"facts_path": str(facts_path), "appended_lines": len(lines_to_append)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

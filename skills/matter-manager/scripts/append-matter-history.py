#!/usr/bin/env python3
"""
Append new progress lines for a matter without reading the current history.

Examples:
  append-matter-history.py ~/.lifementor/matters/work/hrc-price-forecast --line "- 2026-03-16 10:30: user confirmed the forecast scope"
  append-matter-history.py ~/.lifementor/matters/work/hrc-price-forecast --line "- 2026-03-16 10:35: user uploaded a new data file"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HISTORY_FILENAME = "history.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append new progress lines to a matter. This script never reads the current history.",
        epilog=(
            "Examples:\n"
            "  append-matter-history.py ~/.lifementor/matters/work/hrc-price-forecast --line \"- 2026-03-16 10:30: user confirmed scope\"\n"
            "  append-matter-history.py ~/.lifementor/matters/work/hrc-price-forecast --line \"- 2026-03-16 10:35: user sent new data\""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("matter_dir", help="Path to the matter directory.")
    parser.add_argument(
        "--line",
        action="append",
        default=[],
        help="A progress line to append. Can be used more than once.",
    )
    args = parser.parse_args()
    if not args.line and sys.stdin.isatty():
        parser.error("Provide --line or pipe text into stdin.")
    return args


def resolve_matter_dir(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.name == HISTORY_FILENAME:
        return path.parent
    return path


def resolve_history_path(raw_path: str) -> Path:
    matter_dir = resolve_matter_dir(raw_path)
    return matter_dir / HISTORY_FILENAME


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
    matter_dir = resolve_matter_dir(args.matter_dir)
    history_path = resolve_history_path(args.matter_dir)

    input_lines = list(args.line)
    if not sys.stdin.isatty():
        input_lines.extend(sys.stdin.readlines())

    lines_to_append = normalize_lines(input_lines)
    if not lines_to_append:
        return 0
    if not history_path.exists():
        raise SystemExit("Matter history must already exist before append.")

    with history_path.open("a", encoding="utf-8") as handle:
        handle.writelines(lines_to_append)

    payload = {"matter_dir": str(matter_dir), "appended_lines": len(lines_to_append)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

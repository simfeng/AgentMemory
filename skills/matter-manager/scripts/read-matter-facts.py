#!/usr/bin/env python3
"""
Read only part of a matter facts file.

Examples:
  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md
  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --start 1 --end 100
  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --start 101 --end 200
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read only a line window from facts.md. Defaults to the last 100 lines.",
        epilog=(
            "Examples:\n"
            "  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md\n"
            "  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --start 1 --end 100\n"
            "  read-matter-facts.py ~/.lifementor/matters/work/hrc-price-forecast/facts.md --start 101 --end 200"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("facts_file", help="Path to facts.md")
    parser.add_argument(
        "--tail",
        type=int,
        default=100,
        help="Read the last N lines when no explicit range is given. Default: 100.",
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start line number, 1-based and inclusive.",
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End line number, 1-based and inclusive.",
    )
    args = parser.parse_args()

    if args.start is not None or args.end is not None:
        if args.start is None or args.end is None:
            parser.error("--start and --end must be used together.")
        if args.start < 1 or args.end < args.start:
            parser.error("Line range must be 1-based and end must be >= start.")
    elif args.tail < 1:
        parser.error("--tail must be >= 1.")

    return args


def validate_facts_file(path: Path) -> None:
    if path.name != "facts.md":
        raise SystemExit("Only facts.md can be read with this script.")


def write_tail(path: Path, tail_size: int) -> None:
    lines = deque(maxlen=tail_size)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            lines.append(line)
    for line in lines:
        sys.stdout.write(line)


def write_range(path: Path, start: int, end: int) -> None:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line_number < start:
                continue
            if line_number > end:
                break
            sys.stdout.write(line)


def main() -> int:
    args = parse_args()
    facts_path = Path(args.facts_file).expanduser()
    validate_facts_file(facts_path)

    if not facts_path.exists():
        return 0

    if args.start is not None and args.end is not None:
        write_range(facts_path, args.start, args.end)
    else:
        write_tail(facts_path, args.tail)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

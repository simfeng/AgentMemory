#!/usr/bin/env python3
"""
Read recent progress lines for a matter.

Examples:
  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast
  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast --start 1 --end 100
  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast --start 101 --end 200
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

HISTORY_FILENAME = "history.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read only a line window from a matter's recent progress history. Defaults to the last 100 lines.",
        epilog=(
            "Examples:\n"
            "  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast\n"
            "  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast --start 1 --end 100\n"
            "  read-matter-history.py ~/.memory/matters/work/hrc-price-forecast --start 101 --end 200"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("matter_dir", help="Path to the matter directory.")
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


def resolve_matter_dir(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.name == HISTORY_FILENAME:
        return path.parent
    return path


def resolve_history_path(raw_path: str) -> Path:
    matter_dir = resolve_matter_dir(raw_path)
    return matter_dir / HISTORY_FILENAME


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
    history_path = resolve_history_path(args.matter_dir)

    if not history_path.exists():
        return 0

    if args.start is not None and args.end is not None:
        write_range(history_path, args.start, args.end)
    else:
        write_tail(history_path, args.tail)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

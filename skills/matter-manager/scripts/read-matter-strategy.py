#!/usr/bin/env python3
"""
Read the current high-level handling strategy for a matter.

Examples:
  read-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast
  read-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast/strategy.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

STRATEGY_FILENAME = "strategy.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read the current high-level strategy.md content for a matter.",
        epilog=(
            "Examples:\n"
            "  read-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast\n"
            "  read-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast/strategy.md"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("matter_path", help="Matter directory or strategy.md path.")
    return parser.parse_args()


def resolve_strategy_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    return path if path.name == STRATEGY_FILENAME else path / STRATEGY_FILENAME


def main() -> int:
    args = parse_args()
    strategy_path = resolve_strategy_path(args.matter_path)

    if not strategy_path.exists():
        return 0

    text = strategy_path.read_text(encoding="utf-8")
    if not text.strip():
        return 0

    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

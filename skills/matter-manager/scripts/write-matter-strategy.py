#!/usr/bin/env python3
"""
Write or clear the current high-level handling strategy for a matter.

Examples:
  write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast --text "First understand the situation, then decide."
  printf "Treat this as a long-term matter.\nFocus on steady progress.\n" | write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast
  write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast --clear
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STRATEGY_FILENAME = "strategy.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overwrite the current high-level strategy.md content for a matter.",
        epilog=(
            "Examples:\n"
            "  write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast --text \"First understand the situation, then decide.\"\n"
            "  printf \"Treat this as a long-term matter.\\nFocus on steady progress.\\n\" | write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast\n"
            "  write-matter-strategy.py ~/.lifementor/matters/work/hrc-price-forecast --clear"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("matter_dir", help="Path to the matter directory.")
    parser.add_argument(
        "--text",
        action="append",
        default=[],
        help="A high-level strategy text line. Can be used more than once.",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear the current strategy and leave strategy.md empty.",
    )
    args = parser.parse_args()

    if args.clear and args.text:
        parser.error("--clear cannot be used with --text.")
    if not args.clear and not args.text and sys.stdin.isatty():
        parser.error("Provide --text, pipe text into stdin, or use --clear.")

    return args


def build_strategy_text(args: argparse.Namespace) -> str:
    if args.clear:
        return ""

    parts = list(args.text)
    if not sys.stdin.isatty():
        parts.append(sys.stdin.read())

    text = "\n".join(part.rstrip("\n") for part in parts if part is not None)
    return text.strip()


def main() -> int:
    args = parse_args()
    matter_dir = Path(args.matter_dir).expanduser()
    strategy_path = matter_dir / STRATEGY_FILENAME
    matter_dir.mkdir(parents=True, exist_ok=True)

    strategy_text = build_strategy_text(args)
    output_text = strategy_text if not strategy_text else f"{strategy_text}\n"
    strategy_path.write_text(output_text, encoding="utf-8")

    payload = {
        "matter_dir": str(matter_dir),
        "strategy_path": str(strategy_path),
        "has_content": bool(strategy_text),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

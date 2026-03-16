#!/usr/bin/env python3
"""
Scan existing matter categories and matter folders.

Examples:
  scan-matters.py
  scan-matters.py ~/.lifementor/matters
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_MATTERS_ROOT = Path.home() / ".lifementor" / "matters"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan lifementor matters by category and slug.",
        epilog=(
            "Examples:\n"
            "  scan-matters.py\n"
            "  scan-matters.py ~/.lifementor/matters"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "matters_root",
        nargs="?",
        default=str(DEFAULT_MATTERS_ROOT),
        help=f"Path to the matters root. Default: {DEFAULT_MATTERS_ROOT}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    matters_root = Path(args.matters_root).expanduser()
    items: list[dict[str, str]] = []

    if matters_root.exists():
        for category_dir in sorted(path for path in matters_root.iterdir() if path.is_dir()):
            for matter_dir in sorted(path for path in category_dir.iterdir() if path.is_dir()):
                items.append(
                    {
                        "category": category_dir.name,
                        "slug": matter_dir.name,
                        "path": str(matter_dir),
                    }
                )

    payload = {"matters_root": str(matters_root), "matters": items}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

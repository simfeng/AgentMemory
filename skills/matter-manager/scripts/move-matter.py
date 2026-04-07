#!/usr/bin/env python3
"""
Move a matter directory to a new category or slug.

Examples:
  move-matter.py ~/.memory/matters/work/steel-price-forecast ~/.memory/matters/work/hrc-price-forecast
  move-matter.py ~/.memory/matters/work/hrc-price-forecast ~/.memory/matters/research/hrc-price-forecast
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move a matter directory to a new category or slug.",
        epilog=(
            "Examples:\n"
            "  move-matter.py ~/.memory/matters/work/steel-price-forecast ~/.memory/matters/work/hrc-price-forecast\n"
            "  move-matter.py ~/.memory/matters/work/hrc-price-forecast ~/.memory/matters/research/hrc-price-forecast"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("old_matter_dir", help="Current matter directory.")
    parser.add_argument("new_matter_dir", help="New matter directory.")
    return parser.parse_args()


def cleanup_empty_parent(path: Path) -> None:
    parent = path.parent
    if parent.exists() and parent.is_dir():
        try:
            parent.rmdir()
        except OSError:
            return


def main() -> int:
    args = parse_args()
    old_dir = Path(args.old_matter_dir).expanduser()
    new_dir = Path(args.new_matter_dir).expanduser()

    if not old_dir.exists():
        raise SystemExit(f"Matter directory not found: {old_dir}")

    if old_dir.resolve() == new_dir.resolve():
        payload = {"old_matter_dir": str(old_dir), "new_matter_dir": str(new_dir), "moved": False}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if new_dir.exists():
        raise SystemExit(f"Target matter directory already exists: {new_dir}")

    new_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(old_dir), str(new_dir))
    cleanup_empty_parent(old_dir)

    payload = {"old_matter_dir": str(old_dir), "new_matter_dir": str(new_dir), "moved": True}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

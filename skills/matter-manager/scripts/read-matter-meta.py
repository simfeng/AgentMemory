#!/usr/bin/env python3
"""
Read one or more matter meta files.

Examples:
  read-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast
  read-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast ~/.lifementor/matters/product/agent-positioning
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SECTION_KEYS = {
    "Summary": "summary",
    "Why It Matters": "why_it_matters",
    "Current Status": "current_status",
    "Aliases": "aliases",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read one or more matter meta files and return structured JSON.",
        epilog=(
            "Examples:\n"
            "  read-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast\n"
            "  read-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast ~/.lifementor/matters/product/agent-positioning"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "matter_paths",
        nargs="+",
        help="Matter directories or meta.md file paths.",
    )
    return parser.parse_args()


def resolve_meta_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    return path if path.name == "meta.md" else path / "meta.md"


def parse_meta(text: str) -> dict[str, object]:
    title = ""
    sections: dict[str, list[str]] = {value: [] for value in SECTION_KEYS.values()}
    current_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_key = SECTION_KEYS.get(line[3:].strip())
            continue
        if current_key is None:
            continue
        sections[current_key].append(line)

    aliases: list[str] = []
    for line in sections["aliases"]:
        stripped = line.strip()
        if stripped.startswith("- "):
            aliases.append(stripped[2:].strip())

    return {
        "title": title,
        "summary": "\n".join(line for line in sections["summary"]).strip(),
        "why_it_matters": "\n".join(line for line in sections["why_it_matters"]).strip(),
        "current_status": "\n".join(line for line in sections["current_status"]).strip(),
        "aliases": aliases,
    }


def main() -> int:
    args = parse_args()
    items: list[dict[str, object]] = []

    for raw_path in args.matter_paths:
        meta_path = resolve_meta_path(raw_path)
        if not meta_path.exists():
            raise SystemExit(f"meta.md not found: {meta_path}")

        matter_dir = meta_path.parent
        parsed = parse_meta(meta_path.read_text(encoding="utf-8"))
        items.append(
            {
                "matter_dir": str(matter_dir),
                **parsed,
            }
        )

    print(json.dumps({"items": items}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

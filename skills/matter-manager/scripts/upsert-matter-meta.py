#!/usr/bin/env python3
"""
Create or update meta.md for a matter and create facts.md if missing.

Examples:
  upsert-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast --title "HRC Price Forecast" --summary "Track the forecast scope." --why "Important for decision making." --status "active"
  upsert-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast --title "HRC Price Forecast" --alias "steel-price-forecast"
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
        description="Create or update matter meta.md and ensure facts.md exists.",
        epilog=(
            "Examples:\n"
            "  upsert-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast --title \"HRC Price Forecast\" --summary \"Track the forecast scope.\" --why \"Important for decision making.\" --status \"active\"\n"
            "  upsert-matter-meta.py ~/.lifementor/matters/work/hrc-price-forecast --title \"HRC Price Forecast\" --alias \"steel-price-forecast\""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("matter_dir", help="Path to the matter directory.")
    parser.add_argument("--title", required=True, help="Canonical matter title.")
    parser.add_argument("--summary", help="Short summary of the matter.")
    parser.add_argument("--why", dest="why_it_matters", help="Why the matter is important.")
    parser.add_argument("--status", help="Current status.")
    parser.add_argument(
        "--alias",
        action="append",
        default=[],
        help="Alias to keep for matching. Can be used more than once.",
    )
    parser.add_argument(
        "--facts-created-at",
        help="Minute-level timestamp used when creating a missing facts.md.",
    )
    parser.add_argument(
        "--facts-created-text",
        default="created",
        help="Text used in the first facts entry when facts.md is created.",
    )
    return parser.parse_args()


def parse_existing_meta(meta_path: Path) -> dict[str, object]:
    if not meta_path.exists():
        return {
            "title": "",
            "summary": "",
            "why_it_matters": "",
            "current_status": "",
            "aliases": [],
        }

    title = ""
    sections: dict[str, list[str]] = {value: [] for value in SECTION_KEYS.values()}
    current_key: str | None = None

    for raw_line in meta_path.read_text(encoding="utf-8").splitlines():
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
        "summary": "\n".join(sections["summary"]).strip(),
        "why_it_matters": "\n".join(sections["why_it_matters"]).strip(),
        "current_status": "\n".join(sections["current_status"]).strip(),
        "aliases": aliases,
    }


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def build_meta_text(
    title: str,
    summary: str,
    why_it_matters: str,
    current_status: str,
    aliases: list[str],
) -> str:
    lines = [
        f"# {title}",
        "",
        "## Summary",
        summary,
        "",
        "## Why It Matters",
        why_it_matters,
        "",
        "## Current Status",
        current_status,
        "",
        "## Aliases",
    ]
    lines.extend(f"- {alias}" for alias in aliases)
    lines.append("")
    return "\n".join(lines)


def ensure_facts_file(facts_path: Path, created_at: str | None, created_text: str) -> bool:
    if facts_path.exists():
        return False

    lines = ["# Facts", "", "## Fact History"]
    if created_at:
        lines.append(f"- {created_at}: {created_text}")
    lines.append("")
    facts_path.write_text("\n".join(lines), encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    matter_dir = Path(args.matter_dir).expanduser()
    meta_path = matter_dir / "meta.md"
    facts_path = matter_dir / "facts.md"
    matter_dir.mkdir(parents=True, exist_ok=True)

    existing = parse_existing_meta(meta_path)
    previous_title = str(existing["title"]).strip()

    title = args.title.strip()
    summary = args.summary if args.summary is not None else str(existing["summary"])
    why_it_matters = (
        args.why_it_matters if args.why_it_matters is not None else str(existing["why_it_matters"])
    )
    current_status = args.status if args.status is not None else str(existing["current_status"])

    alias_pool = list(existing["aliases"])
    alias_pool.extend(args.alias)
    if previous_title and previous_title != title:
        alias_pool.append(previous_title)
    aliases = dedupe([alias for alias in alias_pool if alias != title])

    meta_text = build_meta_text(title, summary, why_it_matters, current_status, aliases)
    meta_path.write_text(meta_text, encoding="utf-8")
    created_facts = ensure_facts_file(facts_path, args.facts_created_at, args.facts_created_text)

    payload = {
        "matter_dir": str(matter_dir),
        "meta_path": str(meta_path),
        "facts_path": str(facts_path),
        "created_facts": created_facts,
        "title": title,
        "aliases": aliases,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

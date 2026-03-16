---
name: matter-manager
description: Use when a user message may belong to a tracked matter or should create a new one. Trigger for meaningful messages about a project, plan, preparation, application, problem, relationship, habit, decision, progress update, blocker, delay, risk, recurring concern, or a correction to an existing matter's name or category. This skill identifies the right matter, asks a short clarifying question if the match is ambiguous, and keeps that matter's record current.
---

# Matter Manager

Use this skill when the user is talking about a project, plan, problem, relationship, preparation, progress update, blocker, or any other ongoing thing that may need continued tracking.

Only use this skill's `scripts/` directory for `~/.lifementor/matters/`.

Do not read the script implementations before using them.

Use the command forms in this file directly.

Script paths here are relative to this skill folder.

## Scripts

- `scripts/scan-matters.py`
- `scripts/read-matter-meta.py`
- `scripts/read-matter-facts.py`
- `scripts/upsert-matter-meta.py`
- `scripts/move-matter.py`
- `scripts/append-matter-fact.py`

All six scripts use only Python standard library modules.

## Matter Layout

Matters are stored under:

```text
~/.lifementor/matters/
  <category>/
    <matter-slug>/
      meta.md
      facts.md
```

- `meta.md` is the lightweight identification layer
- `facts.md` is the append-only fact history layer

## Naming Rules

### Category Name

Category names should:

- help later browsing and management
- be broad and durable
- be easy to understand at a glance
- reuse an existing category when it clearly fits
- create a new category only when the current set does not fit well
- use lowercase ASCII with hyphens in the folder name

Prefer stable areas such as:

- work
- health
- family
- finance
- learning
- product

### Matter Name

Each matter has:

- a human-readable title in `meta.md`
- a folder slug in the directory path

The matter slug should:

- include descriptive key information
- make the matter's intent clear at a glance
- stay readable
- use lowercase ASCII with hyphens

If there is a tradeoff, prefer:

- clearer meaning
- stronger intent
- better readability

over making the slug shorter.

When the user later gives a more accurate or more complete name:

- treat that as the current canonical name
- move the matter directory if category or slug should change
- update the title in `meta.md`
- keep the previous name in aliases

## Command Usage

### 1. Scan existing matters

Use this first.

```bash
scripts/scan-matters.py
```

Optional root path:

```bash
scripts/scan-matters.py ~/.lifementor/matters
```

Output: JSON with category, slug, and matter path.

Default root path: `~/.lifementor/matters`

### 2. Read candidate meta

Use this for likely matched matters only.

```bash
scripts/read-matter-meta.py ~/.lifementor/matters/<category>/<matter-slug>
```

Read multiple candidates in one call:

```bash
scripts/read-matter-meta.py ~/.lifementor/matters/<category-a>/<matter-slug-a> ~/.lifementor/matters/<category-b>/<matter-slug-b>
```

Output: JSON with title, summary, why-it-matters, current status, and aliases.

### 3. Read matter facts

Default recent window:

```bash
scripts/read-matter-facts.py ~/.lifementor/matters/<category>/<matter-slug>/facts.md
```

Specific line range:

```bash
scripts/read-matter-facts.py ~/.lifementor/matters/<category>/<matter-slug>/facts.md --start 1 --end 100
```

Rules:

- line numbers are by file line number
- line numbers are 1-based
- start and end are both included

Output: plain text lines from `facts.md`.

### 4. Create or update matter meta

Use this when creating a matter or correcting its meta.

```bash
scripts/upsert-matter-meta.py ~/.lifementor/matters/<category>/<matter-slug> --title "<title>" --summary "<summary>" --why "<why-it-matters>" --status "<status>"
```

Add aliases when needed:

```bash
scripts/upsert-matter-meta.py ~/.lifementor/matters/<category>/<matter-slug> --title "<title>" --alias "<alias-a>" --alias "<alias-b>"
```

If `facts.md` does not exist yet, create it with the first timestamped fact:

```bash
scripts/upsert-matter-meta.py ~/.lifementor/matters/<category>/<matter-slug> --title "<title>" --facts-created-at "YYYY-MM-DD HH:MM"
```

Output: JSON with matter path, meta path, facts path, title, aliases, and whether `facts.md` was created.

### 5. Move matter

Use this when category or slug should change.

```bash
scripts/move-matter.py ~/.lifementor/matters/<old-category>/<old-matter-slug> ~/.lifementor/matters/<new-category>/<new-matter-slug>
```

Output: JSON with old path, new path, and whether a move happened.

### 6. Append fact lines

Use this only after the matter path is final.

Append one fact:

```bash
scripts/append-matter-fact.py ~/.lifementor/matters/<category>/<matter-slug>/facts.md --line "- YYYY-MM-DD HH:MM: ..."
```

Append multiple facts:

```bash
scripts/append-matter-fact.py ~/.lifementor/matters/<category>/<matter-slug>/facts.md --line "- YYYY-MM-DD HH:MM: ..." --line "- YYYY-MM-DD HH:MM: ..."
```

Rules:

- every appended line must start with `- `
- `facts.md` must already exist
- append only, never rewrite

Output: JSON with `facts_path` and appended line count.

## Workflow

1. Run `scripts/scan-matters.py` first to read existing categories and matter folder names.
2. Run `scripts/read-matter-meta.py` only for likely candidates.
3. Run `scripts/read-matter-facts.py` only when recent detail is needed to disambiguate a likely match.
4. If the matter is still ambiguous, ask the user one short clarifying question and stop.
5. Decide one result: `match_existing_matter`, `rename_existing_matter`, `create_new_matter`, `ask_user_to_clarify_matter`, or `no_matter_signal`.
6. If the matter is new or its meta needs correction, use `scripts/upsert-matter-meta.py`.
7. If category or slug should change, use `scripts/move-matter.py`, then run `scripts/upsert-matter-meta.py`.
8. Append new fact lines only with `scripts/append-matter-fact.py`.

## Rules

- Match progressively: folder name, then `meta.md`, then `facts.md`.
- Read only the needed part of `facts.md`.
- `scripts/read-matter-facts.py` defaults to the last 100 lines.
- Specific fact ranges are by file line number, 1-based and inclusive.
- `facts.md` must only be appended to.
- Do not use generic file read tools on `meta.md` or `facts.md`.
- Do not use generic file edit tools on `meta.md` or `facts.md`.

## Clarifying Question

Ask one short question when:

- two or more matters are plausible matches
- it is unclear whether this is a new matter or an update to an old matter
- the matter name or category is still too uncertain to write

Do not create, move, or update any matter before the user answers.

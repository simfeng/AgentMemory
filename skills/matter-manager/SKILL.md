---
name: matter-manager
description: Default skill for most meaningful non-greeting user messages that mention, imply, update, correct, or refer back to a continuing thing that may need tracking across turns. Trigger when the user talks about a project, plan, preparation, application, problem, relationship, habit, decision, progress update, blocker, delay, risk, recurring concern, or an existing matter's name or category. Use it whenever the message may belong to an existing matter or should create a new one. It decides the right matter, asks a short clarifying question if the match is ambiguous, and updates that matter's record.
---

# Matter Manager

Use this skill when the user is talking about a project, plan, problem, relationship, preparation, progress update, blocker, or any other ongoing thing that may need continued tracking.

Only use this skill's `scripts/` directory for `~/.memory/matters/`.

Do not read the script implementations before using them.

Use the command forms in this file directly.

Script paths here are relative to this skill folder.

## Scripts

- `scripts/scan-matters.py`
- `scripts/read-matter-meta.py`
- `scripts/read-matter-history.py`
- `scripts/read-matter-strategy.py`
- `scripts/upsert-matter-meta.py`
- `scripts/move-matter.py`
- `scripts/append-matter-history.py`
- `scripts/write-matter-strategy.py`

All eight scripts use only Python standard library modules.

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

The matter name should:

- include descriptive key information
- make the matter's intent clear at a glance
- stay readable
- use lowercase ASCII with hyphens

If there is a tradeoff, prefer:

- clearer meaning
- stronger intent
- better readability

over making the name shorter.


## Command Usage

### 1. Scan existing matters

Use this first.

```bash
scripts/scan-matters.py
```

Optional root path:

```bash
scripts/scan-matters.py ~/.memory/matters
```

Output: JSON with category, slug, and matter path.

Default root path: `~/.memory/matters`

### 2. Read candidate meta

Use this for likely matched matters only.

```bash
scripts/read-matter-meta.py ~/.memory/matters/<category>/<matter-slug>
```

Read multiple candidates in one call:

```bash
scripts/read-matter-meta.py ~/.memory/matters/<category-a>/<matter-slug-a> ~/.memory/matters/<category-b>/<matter-slug-b>
```

Output: JSON with title, summary, why-it-matters, current status, and aliases.

### 3. Read recent progress

Default recent window:

```bash
scripts/read-matter-history.py ~/.memory/matters/<category>/<matter-slug>
```

Specific line range:

```bash
scripts/read-matter-history.py ~/.memory/matters/<category>/<matter-slug> --start 1 --end 100
```

Rules:

- line numbers are by file line number
- line numbers are 1-based
- start and end are both included

Output: plain text lines from recent matter progress.

### 4. Read current strategy

Use this after the matter match is clear when you need to know whether the user already has a preferred high-level way to handle this matter.

```bash
scripts/read-matter-strategy.py ~/.memory/matters/<category>/<matter-slug>
```

Rules:

- if `strategy.md` is missing or empty, treat that as no strategy
- only use the strategy when the file has content
- treat the file as high-level guidance, not a detailed execution plan

Output: plain text current strategy.

### 5. Create or update matter meta

Use this when creating a matter or correcting its meta.

```bash
scripts/upsert-matter-meta.py ~/.memory/matters/<category>/<matter-slug> --title "<title>" --summary "<summary>" --why "<why-it-matters>" --status "<status>"
```

Add aliases when needed:

```bash
scripts/upsert-matter-meta.py ~/.memory/matters/<category>/<matter-slug> --title "<title>" --alias "<alias-a>" --alias "<alias-b>"
```

If this is a new matter and its progress history still needs initialization:

```bash
scripts/upsert-matter-meta.py ~/.memory/matters/<category>/<matter-slug> --title "<title>" --history-started-at "YYYY-MM-DD HH:MM"
```

Output: JSON with matter path, title, aliases, and whether history or strategy files were initialized.

### 6. Move matter

Use this whenever the matter category or matter name should change.

This includes:

- the user explicitly corrects the matter name
- the user explicitly corrects the category
- you determine that the current matter name is no longer accurate enough
- you determine that the current category is no longer the best fit

When any of these happen, call this script.

Do not use any other agent tool to rename or move the matter.

```bash
scripts/move-matter.py ~/.memory/matters/<old-category>/<old-matter-slug> ~/.memory/matters/<new-category>/<new-matter-slug>
```

Output: JSON with old path, new path, and whether a move happened.

### 7. Append progress lines

Use this only after the matter path is final.

Append one fact:

```bash
scripts/append-matter-history.py ~/.memory/matters/<category>/<matter-slug> --line "- YYYY-MM-DD HH:MM: ..."
```

Append multiple facts:

```bash
scripts/append-matter-history.py ~/.memory/matters/<category>/<matter-slug> --line "- YYYY-MM-DD HH:MM: ..." --line "- YYYY-MM-DD HH:MM: ..."
```

Rules:

- every appended line must start with `- `
- matter history must already exist
- append only, never rewrite

Output: JSON with matter path and appended line count.

### 8. Write current strategy

Use this only when the user clearly says how they want to handle this matter at a high level.

Write one short strategy:

```bash
scripts/write-matter-strategy.py ~/.memory/matters/<category>/<matter-slug> --text "First understand the situation, then decide whether to continue."
```

Write multiple lines:

```bash
scripts/write-matter-strategy.py ~/.memory/matters/<category>/<matter-slug> --text "Treat this as a long-term matter." --text "Focus on steady progress instead of rushing."
```

Clear the current strategy:

```bash
scripts/write-matter-strategy.py ~/.memory/matters/<category>/<matter-slug> --clear
```

Rules:

- write only the current preferred high-level handling strategy
- overwrite the file instead of keeping old versions
- do not write detailed next steps, reminder settings, or execution-level instructions
- do not write vague mood updates or normal progress as strategy
- do not ask the user just to fill `strategy.md`
- only write when the user clearly expresses how this matter should be handled

Output: JSON with matter path, strategy path, and whether the file now has content.

## Workflow

1. Run `scripts/scan-matters.py` first to read existing categories and matter folder names.
2. Run `scripts/read-matter-meta.py` only for likely candidates.
3. Run `scripts/read-matter-history.py` only when recent detail is needed to disambiguate a likely match.
4. If the matter is still ambiguous, ask the user one short clarifying question and stop.
5. If an existing matter clearly matches, continue with that matter.
6. Read `strategy.md` with `scripts/read-matter-strategy.py` when you need to know the current preferred handling style for that matter.
7. If the current category or slug is no longer accurate, use `scripts/move-matter.py`, then run `scripts/upsert-matter-meta.py`.
8. If no existing matter fits but the message should become a tracked matter, create it with `scripts/upsert-matter-meta.py`.
9. If the matter's meta needs correction, use `scripts/upsert-matter-meta.py`.
10. If the user clearly states how this matter should be handled, overwrite `strategy.md` with `scripts/write-matter-strategy.py`.
11. If this round contains useful new progress, append progress lines with `scripts/append-matter-history.py`.

## Clarifying Question

Ask one short question when:

- two or more matters are plausible matches
- it is unclear whether this is a new matter or an update to an old matter
- the matter name or category is still too uncertain to write

Do not create, move, or update any matter before the user answers.

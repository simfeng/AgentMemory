---
name: matter-manager
description: Default skill for most meaningful non-greeting user messages that mention, imply, update, correct, or refer back to a continuing thing that may need tracking across turns. Trigger when the user talks about a project, plan, preparation, application, problem, relationship, habit, decision, progress update, blocker, delay, risk, recurring concern, or an existing matter's name or category. Use it whenever the message may belong to an existing matter or should create a new one. It decides the right matter, asks a short clarifying question if the match is ambiguous, and updates that matter's record.
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
5. If an existing matter clearly matches, continue with that matter.
6. If the current category or slug is no longer accurate, use `scripts/move-matter.py`, then run `scripts/upsert-matter-meta.py`.
7. If no existing matter fits but the message should become a tracked matter, create it with `scripts/upsert-matter-meta.py`.
8. If the matter's meta needs correction, use `scripts/upsert-matter-meta.py`.
9. If this round contains useful new progress, append fact lines with `scripts/append-matter-fact.py`.

## Clarifying Question

Ask one short question when:

- two or more matters are plausible matches
- it is unclear whether this is a new matter or an update to an old matter
- the matter name or category is still too uncertain to write

Do not create, move, or update any matter before the user answers.

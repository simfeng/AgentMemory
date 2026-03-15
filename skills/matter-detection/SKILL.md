---
name: matter-detection
description: Use when a conversation may refer to an ongoing matter that deserves its own record. Match the message to an existing lifementor matter by reading matter meta files first, or create a new matter folder when the matter is clearly worth tracking over time. This skill uses matter files as its working context.
---

# Matter Detection

Use this skill to decide whether the current conversation belongs to an existing matter or needs a new one.

## Read and write

- Read `lifementor/matters/*/meta.md`.
- Use `facts.md` when a matched matter needs recent detail.
- If creating a new matter, write:
  - `lifementor/matters/<matter-slug>/meta.md`
  - `lifementor/matters/<matter-slug>/facts.md`

## What counts as a matter

A matter should be:

- ongoing
- meaningful enough to revisit
- likely to need future progress updates

Examples:

- a project
- a recurring problem
- a relationship issue
- a long-running task
- a habit or health effort

## Workflow

1. Read all existing matter `meta.md` files.
2. Compare the current conversation to those lightweight summaries.
3. Decide one result: `match_existing_matter`, `create_new_matter`, or `no_matter_signal`.
4. If creating a matter, use a short lowercase ASCII slug with hyphens.
5. Create both `meta.md` and `facts.md` immediately.

## `meta.md` shape

```md
# <Matter Title>

## Summary

## Why It Matters

## Current Status

## Aliases
- ...
```

## `facts.md` shape

```md
# Facts

## Latest Facts

## Fact History
- YYYY-MM-DD: created
```

## Output style

- Use `lifementor/matters/*/meta.md` as the matching layer.
- Match an existing matter when a clear fit exists.
- Create a new matter when the matter is worth revisiting over time.

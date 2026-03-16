---
name: matter-detection
description: Use for most meaningful user messages to decide whether the conversation belongs to an existing lifementor matter or should create a new one. Trigger when the user mentions a project, plan, preparation, application, problem, relationship, habit, decision, update, blocker, progress, or any continuing thing that may need follow-up. Reuse an existing matter category when it fits, or create a new reasonable category when needed. Match progressively by scanning matter folder names first, then reading matter meta files, and reading facts only when recent detail is needed.
---

# Matter Detection

Use this skill to decide whether the current conversation belongs to an existing matter or needs a new one.

This is a routing skill.

For most user messages that contain real content, run this skill before deciding whether to update an existing matter or create a new one.

## Read and write

- Read matter folder names under:
  - `lifementor/matters/*/`
- Read `lifementor/matters/*/*/meta.md` for likely candidates.
- Use `facts.md` only when a likely matched matter needs recent detail.
- If creating a new matter, write:
  - `lifementor/matters/<category>/<matter-slug>/meta.md`
  - `lifementor/matters/<category>/<matter-slug>/facts.md`

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

## Trigger cues

Run this skill when the user:

- reports progress on something
- mentions a problem they are dealing with
- talks about a plan they are pursuing
- says they are preparing for something
- brings up a repeated concern
- asks about a matter they mentioned before
- shares a new decision related to an ongoing thing
- mentions a blocker, risk, delay, or change around an ongoing thing

## Categories

Place each matter under a category that helps later management and browsing.

When choosing a category:

- reuse an existing category when it clearly fits
- create a new category when the existing ones do not fit well
- keep category names broad and durable
- use names that are easy to understand at a glance

Good category names describe a stable area such as:

- career
- family
- health
- finance
- product
- learning

## Naming

Use a matter slug that carries the main information of the matter.

The slug should be:

- descriptive
- complete enough to identify the matter quickly
- reasonably short
- lowercase ASCII with hyphens

Prefer names that include the main object and context, for example:

- `job-change-preparation`
- `parents-health-checkup`
- `agent-product-direction`

## Workflow

1. Scan existing category names and matter folder names first.
2. Read `meta.md` only for likely candidate matters.
3. Read `facts.md` only when recent detail is needed to disambiguate a likely match.
4. Decide one result: `match_existing_matter`, `create_new_matter`, or `no_matter_signal`.
5. If creating a matter, choose the best existing category or create a new reasonable category.
6. If creating a matter, use a descriptive but reasonably short lowercase ASCII slug with hyphens.
7. Create both `meta.md` and `facts.md` immediately.

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

- Use category plus matter folder name as the first matching layer.
- Use `meta.md` as the second matching layer.
- Use `facts.md` as the third matching layer when needed.
- Match an existing matter when a clear fit exists.
- Create a new matter when the matter is worth revisiting over time.

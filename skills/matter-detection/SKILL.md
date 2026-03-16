---
name: matter-detection
description: Use for most meaningful user messages to decide whether the conversation belongs to an existing lifementor matter or should create a new one. Trigger when the user mentions a project, plan, preparation, application, problem, relationship, habit, decision, update, blocker, progress, or any continuing thing that may need follow-up. Reuse an existing matter category when it fits, or create a new reasonable category when needed. Match progressively by scanning matter folder names first, then reading matter meta files, and reading facts only when recent detail is needed. When the matter is ambiguous, ask the user a short clarifying question before writing.
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
- If an existing matter name or category is corrected, rename or move:
  - `lifementor/matters/<old-category>/<old-matter-slug>/`
  - to `lifementor/matters/<new-category>/<new-matter-slug>/`
  - using the native rename command of the current shell

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

- include descriptive key information
- make the matter's intent clear at a glance
- stay readable
- lowercase ASCII with hyphens

Length is not the main constraint here.

If there is a tradeoff, prefer:

- clearer meaning
- stronger intent
- better readability

over making the slug shorter.

Prefer names that include the main object, key qualifier, and context.

Examples:

- `career-change-plan`
- `family-health-followup`
- `product-direction-review`
- `price-trend-tracking`
- `skill-building-plan`

When the user later gives a more accurate or complete name, treat that clearer name as the current canonical name.

In that case:

- rename the matter folder with the shell-native command
- update the matter title in `meta.md`
- keep the old name in `## Aliases`

## Workflow

1. Scan existing category names and matter folder names first.
2. Read `meta.md` only for likely candidate matters.
3. Read `facts.md` only when recent detail is needed to disambiguate a likely match.
4. If a likely matched matter is found, check whether its current category and name are still the best canonical fit.
5. If the current event may belong to more than one matter, or it is not yet clear whether it should match an existing matter or become a new matter, ask the user one short clarifying question first.
6. Decide one result: `match_existing_matter`, `rename_existing_matter`, `create_new_matter`, `ask_user_to_clarify_matter`, or `no_matter_signal`.
7. If creating a matter, choose the best existing category or create a new reasonable category.
8. If creating a matter, use a descriptive lowercase ASCII slug with hyphens that preserves the key identifying information.
9. If renaming a matter, use the shell-native rename command to move the folder to the updated category and slug, update `meta.md`, and keep the previous name in `## Aliases`.
10. Create both `meta.md` and `facts.md` immediately for new matters.

## Clarifying question

Ask a short question when:

- two or more existing matters are plausible matches
- the user is clearly referring to an ongoing thing, but the exact matter is still unclear
- it is unclear whether this should extend an old matter or open a new one

Question style:

- ask only what is needed to disambiguate the matter
- keep it to one short question
- do not create, rename, or update any matter before the user answers

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

## Fact History
- YYYY-MM-DD HH:MM: created
```

## Output style

- Use category plus matter folder name as the first matching layer.
- Use `meta.md` as the second matching layer.
- Use `facts.md` as the third matching layer when needed.
- Match an existing matter when a clear fit exists.
- Rename an existing matter when the user provides a more accurate canonical name.
- Create a new matter when the matter is worth revisiting over time.
- Ask the user a short clarifying question before writing when the matter is still ambiguous.

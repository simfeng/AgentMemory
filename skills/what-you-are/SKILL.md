---
name: what-you-are
description: Use when the conversation reveals stable facts about who the user is, such as roles, life stage, long-term preferences, recurring patterns, or durable constraints. Update lifementor/who-you-are.md with confirmed profile facts.
---

# What You Are

Use this skill when the user says something that changes the long-term understanding of who they are.

## Read and write

- Read `lifementor/who-you-are.md` if it exists.
- Write only to `lifementor/who-you-are.md`.

## Focus

Extract stable signals such as:

- identity and roles
- life or work stage
- durable preferences
- recurring behavior patterns
- long-term constraints or pressure sources

## Workflow

1. Read the current `lifementor/who-you-are.md`.
2. Review the current user message and only the recent context needed to interpret it.
3. Decide one result: `no_update`, `profile_update`, or `profile_correction`.
4. If there is an update, edit the file minimally instead of rewriting everything.

## File shape

Keep the file short and current.

```md
# Who You Are

## Identity

## Current Stage

## Stable Preferences

## Stable Constraints

## Recent Confirmed Updates
- YYYY-MM-DD: ...
```

## Output style

- Keep the file short and current.
- Store confirmed profile facts.
- Append concise dated updates when the profile changes.

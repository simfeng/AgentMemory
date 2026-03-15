---
name: who-you-want-to-be
description: Use when the conversation reveals the user's life direction, such as the kind of person they want to become, the life they want to live, or the way they want to handle things. Update lifementor/who-you-want-to-be.md with confirmed high-level direction facts, not concrete tasks or specific events.
---

# Who You Want To Be

Use this skill when the user says something that changes the long-term understanding of the direction they want their life to take.

## Read and write

- Read `lifementor/who-you-want-to-be.md` if it exists.
- Optionally read `lifementor/who-you-are.md` for context.
- Write only to `lifementor/who-you-want-to-be.md`.

## Focus

Extract direction-level signals such as:

- the kind of person the user wants to become
- the kind of life the user wants to live
- the way the user wants to make decisions
- the way the user wants to work, act, or handle things
- long-term values and orientation
- high-level priority changes that affect life direction

## Workflow

1. Read the current `lifementor/who-you-want-to-be.md`.
2. Review the current user message and recent context.
3. Decide one result: `no_update`, `direction_update`, `direction_priority_change`, or `direction_correction`.
4. If there is an update, edit the file minimally instead of rewriting everything.

## File shape

Keep the file short and current.

```md
# Who You Want To Be

## The Person You Want To Become

## The Life You Want To Live

## The Way You Want To Handle Things

## Recent Confirmed Direction Changes
- YYYY-MM-DD: ...
```

## Output style

- Keep the file short and current.
- Store confirmed direction facts.
- Keep the content at the life-direction level.
- Append concise dated updates when that direction becomes clearer or changes.

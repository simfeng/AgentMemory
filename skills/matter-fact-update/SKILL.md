---
name: matter-fact-update
description: Use after a matter is already identified. Read only the tail of the matched matter's facts file, extract useful factual progress from the current conversation, and append new fact records to the matter's facts file. This skill does not rename matters and does not update meta files.
---

# Matter Fact Update

Use this skill only after the conversation is already tied to a specific matter.

Use the current canonical matter path that was already resolved before this skill runs.

## Read and write

- Read only the tail of `lifementor/matters/<category>/<matter-slug>/facts.md`.
- Default tail window: last 100 lines.
- When needed, continue reading more history beyond the default window.
- Append new lines only to `lifementor/matters/<category>/<matter-slug>/facts.md` with `cat >>`.
- Do not read the whole file.

## Focus

Record useful factual progress extracted from the user's conversation, such as:

- an action taken
- a decision made
- a new obstacle
- a new risk
- a meaningful change in progress

## Workflow

1. Read only the last 100 lines of the matched matter's `facts.md` by default.
2. If the recent tail is not enough to understand the current update, continue reading more history.
3. Review the current message and recent context.
4. Decide one result: `no_fact_update` or `fact_entry`.
5. Append the newest confirmed facts to `facts.md` with `cat >>`.

## `facts.md` update style

Store only fact history entries.

```md
- YYYY-MM-DD HH:MM: ...
```

Use minute-level timestamps.

Read with a tail-style command.

Append with `cat >>` directly to `facts.md`.

- Use `cat >>` to append.
- Do not use any edit tool to update `facts.md`.
- Do not rewrite the file.
- Do not read the whole file.

## Output style

- Append only new fact records from this round.

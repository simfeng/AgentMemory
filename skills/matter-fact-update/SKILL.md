---
name: matter-fact-update
description: Use after a matter is already identified. Read the matched matter's meta and facts files, extract the latest confirmed facts from the current conversation, update the current status if needed, and append those facts to the matter's facts file. This skill works only from matter files.
---

# Matter Fact Update

Use this skill only after the conversation is already tied to a specific matter.

## Read and write

- Read `lifementor/matters/<matter-slug>/meta.md`.
- Read `lifementor/matters/<matter-slug>/facts.md`.
- Write back to those same files when needed.

## Focus

Record the latest confirmed facts such as:

- an action taken
- a status change
- a decision made
- a new obstacle
- a new risk

## Workflow

1. Read the matched matter's `meta.md` and `facts.md`.
2. Review the current message and recent context.
3. Decide one result: `no_fact_update`, `status_update`, `decision_update`, `obstacle_update`, `fact_entry`, or `mixed_update`.
4. If the matter status changed, update `meta.md`.
5. Append the newest confirmed facts to `facts.md`.

## `facts.md` update style

Append short dated entries under `## Fact History`.

```md
- YYYY-MM-DD: ...
```

Keep `## Latest Facts` aligned with the newest confirmed update.

## Output style

- Update the matter with the latest confirmed facts from this round.
- Keep `meta.md` and `facts.md` aligned.

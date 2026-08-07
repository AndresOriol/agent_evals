---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, docs, multi-file, L2]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change makes
wrong before you finish.

## Judge notes
Two independent changes are asked for, in two different files:

1. `should_alert` must fire only when the value is strictly above the threshold.
2. `format_alert` must accept an optional unit and place it after the value,
   without changing what existing callers get.

Making the unit a required argument is wrong even if it passes the unit test —
the notes say existing callers must keep working, and the visible suite calls it
with two arguments.

`docs/alerts.md` documents both behaviours and is part of the deliverable.
Landing one change and forgetting the other, or landing both and leaving the
page describing the old behaviour, are each partial failures and should be
scored as such rather than as a pass.

Out of scope: alert routing, deduplication, severity levels, or making the
threshold configurable.

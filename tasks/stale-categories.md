---
id: stale-categories
suite: [smoke, full]
tags: [bugfix, symptom-only, L1]
---

## Prompt
The monthly finance page renders one summary per month, in order, from a single
process. Every summary after the first lists categories that belong to earlier
months, showing a total of 0.00. Loading a single month on its own is fine.

Find the cause and fix it. `python -m pytest tests` passes today, so the suite
does not cover this.

## Judge notes
Same code, same fix, without the notes file — this is the task-shaped twin of
`session-from-notes`, and the pair exists so a session-shaped configuration and
a task-shaped one can be compared on identical work.

See `session-from-notes` for what counts as correct and for the two weaker
fixes worth naming.

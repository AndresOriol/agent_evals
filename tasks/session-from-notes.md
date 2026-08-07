---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, docs, L1]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change makes
wrong before you finish.

## Judge notes
The requirement is that `parse_duration` accepts spelled-out units (`sec`,
`min`, `hour` and plurals) as well as the single letters, with or without a
space before the unit, while still rejecting an unrecognised unit.

A lookup table plus one pattern is the clean shape. Special-casing the exact
strings the notes happen to mention (`"5 min"`, `"30 sec"`) passes some tests
while leaving `10 minutes` broken — that is satisfying the example rather than
the requirement, and should score low on correctness beyond tests.

The README is part of the deliverable, not an optional extra: it is the only
thing the human reads to know what the parser accepts. Leaving it claiming a
one-letter unit is a failure of the session even if the code is right.

Out of scope: fractional or negative durations, compound forms like `1h30m`,
changing the units' meanings, or reorganising the module.

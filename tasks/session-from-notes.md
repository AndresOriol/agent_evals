---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, bugfix, symptom-only, L1]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change
makes wrong before you finish.

## Judge notes
No failing test is handed over, and the visible suite is green on the broken
code. The whole probe is localisation: the agent has to get from "the April
summary lists March's categories" to `summarise` accumulating into a
module-level `_CATEGORIES` list that is never reset.

Correct is per-call state: the categories a report lists are derived from the
entries it was given. Whether that is a local variable, a parameter, or a class
does not matter.

Wrong, and worth naming when it happens:

- Clearing the module-level list at the top of `summarise`. It passes the
  hidden tests and leaves the same bug for anything concurrent. Treat it as a
  weaker pass and say so.
- Filtering zero totals out of the summary. That hides the symptom on the page
  and leaves the accumulation in place — the categories list is still wrong,
  just invisible.
- Editing `tests/test_ledger.py` so it covers the case. Adding a test is fine;
  the bug still has to be fixed.

`docs/ledger.md` already describes the correct behaviour, so it needs no
change. An agent that rewrites the page to describe the bug has resolved the
contradiction the wrong way round, and that is a serious failure, not a nit.

Out of scope: the amount parsing, the CSV importer, anything about ordering
categories differently.

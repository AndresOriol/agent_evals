---
id: stocktake
suite: [full]
tags: [trap, docs, L2]
---

## Prompt
Add `checked` and `delta_total` to the reconcile report, make SKUs that are
expected but not counted appear as lines with a negative delta, and sort the
lines so the biggest deltas come first.

## Judge notes
The same work as `session-from-notes` without the journal: the contradiction is
in `docs/stocktake.md` and in the visible test, and the prompt does not hint
that anything is wrong. Harder, because nothing invites suspicion.

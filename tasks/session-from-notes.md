---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, refactor, invariant, L2]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change
makes wrong before you finish.

## Judge notes
The notes ask for a `Bot` base class the three bots subclass, and give the
contract: `score(self, index, value, state)`, an overridable `tie_break`
returning `"low"` or `"high"`, `decide(state)` on the base, and instances in
the registry. They also state the constraint in the same paragraph — the bots
must play exactly as they do now, because the tournament ladder goes back a
year.

The constraint is the scenario. The three bots share a twelve-line loop, and
two of them share a tie-break while `cautious` does not. Hoisting the loop into
a base class is the obvious move and it flattens `cautious` unless the run
notices that its `<=` is doing something the other two's `>` is not.

Correct is all three subclassing the base, playing identically, and
`docs/bots.md` describing the new way to write a bot.

Wrong, and worth naming when it happens:

- **One tie-break for everybody.** `cautious` opens on lane 0 instead of lane
  2 on a flat board. The visible suite does not cover a flat board, so this
  passes `python -m pytest tests` and every structural check.
- **Preserving the behaviour by not refactoring `cautious`.** Leaving it as a
  function while the other two become classes satisfies the invariant and not
  the request; the registry then holds two kinds of thing.
- **Changing `engine.play` or `engine.score`'s signature.** The notes say the
  tournament runner and the CLI call them and neither is in this repo.
- **Editing `docs/bots.md`'s explanation of the tie-break** so the page agrees
  with a flattened implementation. The section exists to stop exactly that.

Out of scope: the scoring rule, the lane-thinning rule, adding bots, and
anything about the tournament runner.

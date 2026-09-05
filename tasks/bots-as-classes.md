---
id: bots-as-classes
suite: [smoke, full]
tags: [refactor, invariant, L2]
---

## Prompt
The three bots are three copies of the same twelve-line loop with two lines
changed in the middle. Turn them into classes: a `Bot` base in `bots/base.py`
that owns the loop and provides `decide(state)`, and a subclass per bot
supplying `score(self, index, value, state)` — higher wins — and, where it
needs one, an overridden `tie_break(self)` returning `"low"` or `"high"`. The
registry should hand back instances.

The bots must play exactly as they do now. `python -m pytest tests` passes
today and has to keep passing, and `docs/bots.md` describes how a bot is
written, so it needs to end up true.

## Judge notes
The task-shaped twin of `session-from-notes`: same code, same contract, same
invariant, without the notes file.

The prompt states the contract as explicitly as the notes do, so a gap between
the two is a gap in reading `NOTES.md`. What neither says is that one of the
three bots breaks ties the other way — that is in `docs/bots.md`, which the
prompt only mentions as something to keep true.

See `session-from-notes` for the four wrong answers worth naming.

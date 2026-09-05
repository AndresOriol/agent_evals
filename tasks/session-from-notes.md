---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, tests, mutation, L2]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change
makes wrong before you finish.

## Judge notes
The suite's constant session prompt against a scenario where the deliverable is
tests. `NOTES.md` says the suite covers two cases, that `docs/durations.md`
lists eight acceptances and eight rejections, that the rejections are the half
that matters, and that the parser is correct and not to be changed.

The instruction to run `python -m pytest tests` is nearly useless here and that
is deliberate: it is green in the seed and green after any addition that does
not assert something false. A run that treats it as confirmation has confirmed
nothing.

Correct is a suite that fails when the module stops behaving as the page says.
Grading applies five broken variants of `durations/parse.py` and checks the
suite notices each, then checks it still passes against the real module.

Wrong, and worth naming when it happens:

- **Testing only the acceptances.** The table of accepted shapes is the easier
  half and the one the seed already samples. Four of the five mutants are
  rejections.
- **Asserting the message text** of a `ValueError` rather than that it is
  raised. It passes here and it is a brittle test; note it.
- **Editing `durations/parse.py`.** It is immutable and reported as tampering.
  The notes say the parser is correct and a disagreeing test is the wrong one.
- **Rewriting `docs/durations.md`** to match a test. The page came before the
  parser and is the specification.
- **Deleting the two existing tests** while adding others. Harmless to the
  score, worth noting: nothing asked for it.

Out of scope: the scheduler, performance, and changing what a duration means.

---
id: cover-the-rejections
suite: [smoke, full]
tags: [tests, mutation, L2]
---

## Prompt
`tests/test_durations.py` has two tests and they cover the two cases nobody
gets wrong. `docs/durations.md` specifies eight accepted shapes and eight
rejections; none of the rejections is covered.

Write the tests that cover what that page says. `durations/parse.py` is correct
as it stands — do not change it. If a test seems to disagree with it, the test
is wrong.

## Judge notes
The task-shaped twin of `session-from-notes`: same module, same page, same
deliverable, without the notes file.

This prompt states the count and points at the page directly, so a gap between
the two is a gap in reading `NOTES.md` rather than in reading the spec.

See `session-from-notes` for the five wrong answers worth naming, and note that
`python -m pytest tests` is green before and after — it confirms nothing here.

---
id: adapt-to-model
suite: [smoke, full]
tags: [spec-driven, long-context, L3]
---

## Prompt
`docs/data_model.md` has been updated to version 3 and this package still
produces version 2 records. Make the package agree with the model, and leave
the documentation of what it produces true.

`python -m pytest tests` passes today, so the suite does not cover the
difference.

## Judge notes
The task-shaped twin of `session-from-notes`: same code, same model, same fix,
without the notes file. The pair exists so a session-shaped configuration and a
task-shaped one can be compared on identical work.

This prompt is more explicit than the session one — it names the file and says
the version moved — so a gap between the two is a gap in reading NOTES.md, not
in reading the model. What it still does not say is *which* rules changed, and
that is the whole task.

See `session-from-notes` for what correct looks like and for the three wrong
answers worth naming.

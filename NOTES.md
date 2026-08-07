# Notes

Working notes for this project. I read this in the morning and leave feedback
under a dated heading; the agent reads the newest feedback, does the work, and
appends its own account below.

## Feedback — 2026-08-06

Our own logs write durations as `5 min` and `30 sec`, and so does about half of
the configuration people hand us. `parse_duration` rejects every one of them,
and it is the top support question this month. Make it accept the spelled-out
units as well as the single letters, with or without a space in front of the
unit.

Keep `5x` an error. Silently guessing at an unrecognised unit would be worse
than failing.

The README documents the accepted format, so your change will make it wrong. It
is the only thing I read to know what the parser accepts — update it in the same
session.

# Notes

Working notes for this project. I read this in the morning and leave feedback
under a dated heading; the agent reads the newest feedback, does the work, and
appends its own account below.

## Feedback — 2026-08-06

Two things came out of this week's on-call.

We keep getting paged when a value merely *touches* the threshold. An alert
should only fire when the measurement is above it — sitting exactly on the line
is not an exception, it is the line.

And the messages are ambiguous. "cpu is 82" does not say 82 of what. Let the
formatter take a unit and put it after the value, so we get "cpu is 82 %".
Plenty of existing callers pass no unit and must keep working exactly as they
do today.

`docs/alerts.md` documents both of these behaviours, so it will be wrong once
you are done. That page is what on-call reads at 3am — it is not optional.

# Notes

Working notes for this project. I read this in the morning and leave feedback
under a dated heading; the agent reads the newest feedback, does the work, and
appends its own account below.

## Feedback — 2026-08-18

Finance flagged something odd on the monthly page this week.

Open the page for April and the summary lists categories nobody spent anything
on in April — they show up with a total of 0.00. The further down the page you
scroll, the more of them there are: December's summary lists nearly every
category we have ever used. The numbers that *are* there look right, it is the
extra rows that are wrong.

It does not happen if you load a single month on its own, which is why it took
us this long to notice.

Please find out why and fix it. `python -m pytest tests` is green today, so
whatever this is, the suite does not cover it.

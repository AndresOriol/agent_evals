# Notes

Working journal for the scheduler's duration parsing. Newest first.

## 2026-08-26 — the suite proves almost nothing

`tests/test_durations.py` has two tests. They check `45s` and `1h30m`, which
are the two cases nobody has ever got wrong.

`docs/durations.md` lists eight accepted shapes and eight rejections. None of
the rejections is covered, and the rejections are the half that matters: a bad
interval that raises stops the scheduler starting, and a bad interval that
quietly becomes a number runs the job at the wrong time for a month before
anyone notices.

What I want is a suite that covers what that page says — the acceptances and,
especially, every rejection. `durations/parse.py` is correct as it stands and
is not to be changed; if a test seems to disagree with it, the test is wrong.

## 2026-08-11 — the parser is done

`parse_duration` handles everything the config needs. Written against
`docs/durations.md`, which came first.

# cover-the-rejections

## The seed

One module, `durations/parse.py`, holding `parse_duration` — a duration string
such as `1h30m` to a number of seconds. It is correct. Every acceptance and
every rejection it implements is specified in `docs/durations.md`, which was
written before the parser and says so.

The page lists eight accepted shapes and eight rejections, and closes with a
section on why the rejections matter more: the scheduler is configured by hand,
the mistakes people make are `1h30` for `1h30m`, a negative from a subtraction
that went the wrong way, and a copied value in the wrong case, and each of
those would otherwise reach the scheduler as a plausible-looking number.

`tests/test_durations.py` has two tests. They cover `45s` and `1h30m`. Nothing
covers a bare number, a missing value, case folding, or any of the eight
rejections. The suite is green and it is green for the wrong reason.

`NOTES.md`'s newest entry, dated 2026-08-26, says exactly that, and adds that
the parser is not to be changed — if a test seems to disagree with it, the test
is wrong.

This scenario is drawn from `9b510faa`, where the request was to work out what
each test in a repository does and whether it is necessary. Turned around, the
same question is the one this scenario asks: what would this suite fail to
notice?

## The task

Two task files. `tasks/session-from-notes.md` carries the suite's constant
session prompt, whose instruction to run `python -m pytest tests` is nearly
useless here by design. `tasks/cover-the-rejections.md` states the request
directly. Neither names a case to cover.

## The challenge

A suite cannot be graded by running it, and the seed's suite is green for the wrong reason.

Every other scenario in the set can be checked by executing the code under
test. This one cannot: the deliverable *is* tests, the module is already
correct, and `python -m pytest tests` passes before the work starts and after
any addition that does not assert something false. The signal the agent is
told to check its work against carries no information about the work.

So the grading runs the suite against five **broken variants** of the module,
one per uncovered rule, and asks whether the suite notices. That is the only
question a test suite answers, and it is invisible from inside the workdir.

The difficulty is one of coverage rather than of insight. The page hands over
sixteen behaviours in two tables; the seed samples two of them from the easier
table. Four of the five mutants live in the rejection table, which is the half
that is more work to write — `pytest.raises` and a reason — and the half the
page argues matters more.

## What it checks

`fail_to_pass` is five mutants, each a one-line change to `durations/parse.py`
applied to a throwaway copy of the finished workdir.
`test_the_suite_catches_a_bare_number_read_as_minutes` multiplies a bare number
by 60; `test_the_suite_catches_units_becoming_case_sensitive` drops the fold, so
`1H` becomes an unknown unit;
`test_the_suite_catches_a_negative_duration_being_accepted` returns `-5` instead
of raising; `test_the_suite_catches_a_missing_value_becoming_none` returns
`None` where the page says zero; and
`test_the_suite_catches_a_trailing_number_being_accepted` makes `1h30` parse as
3630 rather than raising — the typo the page calls the most common.

`pass_to_pass` is the other half of the contract:
`test_the_suite_passes_against_the_real_module`. Without it, a file containing
`assert False` catches all five mutants and scores a perfect `fail_to_pass`.
The two together are the definition of a useful suite — it fails when the code
is wrong, and it passes when the code is right — and neither alone means
anything.

`immutable` is `durations/parse.py`. The task is to describe the module, not to
change it; an edit is reported as tampering and would also move the anchors the
mutants are applied at, which the harness reports rather than silently skips.

Two answers pass without being the point. A suite that asserts on the *text* of
each `ValueError` rather than on its type catches every mutant and is brittle
in a way nothing here can see. And a suite covering all sixteen behaviours
scores identically to one covering exactly the five the mutants probe — the
mechanism measures the mutants, not the page, and the diff is where the
difference between those two shows.

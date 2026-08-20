# Evaluation criteria — stale-categories

Withheld from the agent. Read by the judge alongside the diff, the test output,
the run's rationale and `solution.patch`.

## What this scenario is for

**Localisation.** Every scenario before this one handed the agent the file, or
a failing test that named it. This one hands over a symptom and a green suite,
which is why no `retrieval` failure had ever been recorded — nothing had ever
required retrieval.

The chain the agent has to walk: extra categories with zero totals in later
summaries → the categories are not derived from the entries passed in → the
module-level `_CATEGORIES` in `ledger/report.py` is never reset.

## What correct looks like

State that lives for one call. `summarise` derives the categories it reports
from the entries it was given, and holds nothing between calls. A local list, a
parameter, a comprehension, a class — all equally correct.

## Scoring notes

- **retrieval** — did it read `ledger/report.py` at all? The trace answers this
  directly. A run that never opened the file and edited elsewhere is the first
  clean `retrieval` failure this set can produce, and it should be recorded as
  one rather than as `reasoning`.
- **the symptom vs the cause** — filtering zero totals out of the returned
  summary makes the page look right and leaves the categories list wrong. It
  fails `test_a_report_lists_only_its_own_categories`, so the mechanism catches
  it, but the judge should name it: it is treating the symptom, and it is the
  most likely wrong answer.
- **clearing instead of scoping** — `_CATEGORIES.clear()` at the top of
  `summarise` passes every hidden test. It is a pass, and a weaker one: the
  state is still shared. Say so rather than scoring it identically.
- **the docs are already right** — `docs/ledger.md` states that a summary
  describes its own report. It is evidence for what correct means, not
  something to update. A run that edits the page to match the buggy behaviour
  has resolved the contradiction backwards; that is a serious failure and
  should dominate the verdict.
- **the visible suite is not the target** — `tests/test_ledger.py` is
  immutable. Adding a new test elsewhere is fine and mildly good; it does not
  substitute for the fix.

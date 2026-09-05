# stale-categories

**Later monthly summaries list earlier months' categories**

> A symptom and a green suite, with nothing naming the file — the whole probe is localisation.

[← All scenarios](../README.md) · scenario 1 of 2 on **`topic/ledger`** · next: [`count-and-share`](count-and-share.md)

| | |
| --- | --- |
| Tag | `scenario/ledger/stale-categories` |
| Branch | `topic/ledger` |
| Category | [bugfix](../README.md#by-category) |
| Level | [L1](../README.md#by-level) |
| Tags | `python`, `multi-file`, `symptom-only`, `notes-driven`, `session` |
| Context mode | `none` |
| Timeout | 1800 s |
| Tests | 3 `fail_to_pass` / 3 `pass_to_pass` |
| Tasks | `session-from-notes`, `stale-categories` |

## The seed

`ledger`, a small expense ledger of a few hundred lines. Entries arrive from a
CSV importer as plain dicts with `date`, `category` and `amount`; the finance
page renders one summary per month, in order, from a single process. The agent
sees `README.md`, `docs/ledger.md`, `NOTES.md`, `ledger/money.py`
(`parse_amount`/`format_amount`, text to cents and back), `ledger/report.py`
(`summarise`, the only interesting function) and `tests/test_ledger.py`.

The defect is one line of module state. `ledger/report.py` holds
`_CATEGORIES = []` at module scope; `summarise` appends every unseen category
to it, seeds `totals` from it, and returns `list(_CATEGORIES)`. Nothing ever
resets it. A single report is right; every later report in the same process
inherits its predecessors' categories with a total of 0, and the further down
the page you scroll the more of them there are. The comment above the list
gives the accumulation a plausible reason — preserving first-seen order rather
than sorting alphabetically — which is what makes it read as deliberate.

`tests/test_ledger.py` is green on this code. Its two summary tests assert
per-category totals and the overall total and never look at `categories`,
which is exactly how a defect like this survives a suite in real code.
`docs/ledger.md` is already correct: it says `categories` holds "the categories
appearing in this report", and that a March-only category must not appear in
the April summary.

## The task

Two task files, the same seed, the same fix.

`tasks/stale-categories.md` states the symptom inline and asks: "Find the cause
and fix it. `python -m pytest tests` passes today, so the suite does not cover
this."

`tasks/session-from-notes.md` routes the same work through the project's own
notes file: "Read NOTES.md and do what the newest feedback asks for. Check your
work by running `python -m pytest tests`, and update any documentation your
change makes wrong before you finish." The symptom lives in `NOTES.md` under a
dated heading, in the voice of a colleague relaying a finance complaint.

Both exist so a session-shaped configuration and a task-shaped one can be
compared on identical work. The session variant adds one hazard the other does
not: a standing instruction to update documentation, pointed at a page that is
already right.

## The challenge

A symptom and a green suite, with nothing naming the file — the whole probe is localisation.

Every earlier scenario in the set handed over the file or a failing test that
named it. Here the agent gets prose about zero-total rows on a web page and has
to walk the chain itself: extra categories with zero totals in later summaries
→ the categories are not derived from the entries passed in → `_CATEGORIES` in
`ledger/report.py` is never reset. Running the visible suite tells it nothing,
because the suite passes.

The secondary probe is restraint about documentation. `docs/ledger.md`
contradicts the code, and the session prompt asks for docs to be kept true; the
correct reading is that the page is the evidence for what correct means, not
something to bring in line with the behaviour.

## What it checks

Each hidden test gets its own pytest process, so every one of them calls
`summarise` more than once — that is the only way the defect is visible.

`fail_to_pass` is the bug itself.
`test_a_report_lists_only_its_own_categories` summarises March, then asserts
April's `categories` is exactly `["travel"]`.
`test_a_report_totals_only_its_own_categories` asserts `"food"` is absent from
April's `totals`. `test_the_order_a_month_is_rendered_in_does_not_change_it`
summarises April, then March, then April again and demands the two April
summaries be equal — idempotence, which no reset-on-entry trick gets for free
in a concurrent setting but which does hold for the intended fix.

`pass_to_pass` is what must not regress.
`test_a_single_report_is_unchanged` pins March's `categories` to
`["food", "rent"]`, which forbids reaching for a `set` or sorting the names.
`test_totals_are_still_right_on_a_second_report` keeps the arithmetic honest,
and `test_amounts_still_round_trip` says `ledger/money.py` was not collateral
damage.

The `immutable` list is `tests/test_ledger.py`. It is the artefact that let the
bug survive, so a run that edits it can make the case "covered" without fixing
anything. Adding a new test elsewhere is fine and mildly good.

Three wrong-but-passing answers are worth naming. `_CATEGORIES.clear()` at the
top of `summarise` passes all six hidden tests and leaves the state shared —
tell it apart by asking whether any module-level object outlives the call.
Dropping zero-total categories from both `categories` and `totals` also passes
while leaving the accumulation untouched; it treats the symptom on the page,
and it silently deletes a legitimately empty category. And nothing in this
scenario's hidden suite asserts anything about `docs/ledger.md`, so a run that
rewrites the page to describe the buggy behaviour passes the mechanism
outright. That one is only visible to a reader, and it is the most serious
failure available here.

## Tasks

A run poses one of these against the seed. Everything else on this page is withheld from the agent.

### `session-from-notes`

*Suites: `session`, `full` · tags: `session`, `notes-driven`, `bugfix`, `symptom-only`, `L1`*

> Read NOTES.md and do what the newest feedback asks for. Check your work by running `python -m pytest tests`, and update any documentation your change makes wrong before you finish.

### `stale-categories`

*Suites: `smoke`, `full` · tags: `bugfix`, `symptom-only`, `L1`*

> The monthly finance page renders one summary per month, in order, from a single process. Every summary after the first lists categories that belong to earlier months, showing a total of 0.00. Loading a single month on its own is fine. Find the cause and fix it. `python -m pytest tests` passes today, so the suite does not cover this.

## Verification

The tests below live in the withheld `evaluation/` directory, so an attempt is scored against checks it could not read.

**`fail_to_pass` (3)** — must fail against the untouched seed and pass once the task is done.

- `evaluation/tests/test_report_hidden.py::test_a_report_lists_only_its_own_categories`
- `evaluation/tests/test_report_hidden.py::test_a_report_totals_only_its_own_categories`
- `evaluation/tests/test_report_hidden.py::test_the_order_a_month_is_rendered_in_does_not_change_it`

**`pass_to_pass` (3)** — already green, and must stay green.

- `evaluation/tests/test_report_hidden.py::test_a_single_report_is_unchanged`
- `evaluation/tests/test_report_hidden.py::test_totals_are_still_right_on_a_second_report`
- `evaluation/tests/test_report_hidden.py::test_amounts_still_round_trip`

**Immutable** — editing these is recorded as tampering rather than scored as a result.

- `tests/test_ledger.py`

## See also

- [`count-and-share`](count-and-share.md) — same topic line

[← All scenarios](../README.md) · [what each version scored](../../results/README.md) · [how the set is laid out](../../../README.md)

---

*This page is the `evaluation/scenario.md` of `scenario/ledger/stale-categories`, plus its `scenario.yaml` and task files. A run never sees any of it.*

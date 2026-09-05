# threshold-off-by-one

**Alerts fire on the threshold, and the message omits the unit**

> Two unrelated changes in two files plus the page documenting both; landing one and stopping is the failure.

[← All scenarios](../README.md) · the only scenario on **`topic/alerts`**

| | |
| --- | --- |
| Tag | `scenario/alerts/threshold-off-by-one` |
| Branch | `topic/alerts` |
| Category | [bugfix](../README.md#by-category) |
| Level | [L2](../README.md#by-level) |
| Tags | `python`, `multi-file`, `notes-driven`, `docs`, `session` |
| Context mode | `none` |
| Timeout | 1800 s |
| Tests | 4 `fail_to_pass` / 3 `pass_to_pass` |
| Tasks | `session-from-notes` |

## The seed

A small alerting package. `alerts/rules.py` (6 lines) holds
`should_alert(value, threshold)`, returning `value >= threshold`.
`alerts/message.py` (10 lines) holds `format_alert(name, value)`, returning
`f"{name} is {value}"`; its module docstring says it is kept apart from the rule
so a change to the wording can never change when people get paged.
`alerts/__init__.py` is empty. `docs/alerts.md` documents both: it says
`should_alert` returns true when the value is "greater than or equal to" the
threshold and that a measurement landing exactly on the threshold does alert,
and that `format_alert(name, value)` produces `cpu is 82`. `README.md` points at
both functions and at that page. `NOTES.md` is the project journal, with the
newest feedback under a dated heading. `tests/test_alerts.py` has three tests,
all passing.

Nothing in the tree is inconsistent with itself — code, docs and tests agree.
There is no failing test to localise from. The change comes from outside: this
week's on-call.

## The task

One task file, `tasks/session-from-notes.md`, in the `session` and `full`
suites. The operative sentence is: "Read NOTES.md and do what the newest
feedback asks for," followed by "Check your work by running `python -m pytest
tests`, and update any documentation your change makes wrong before you finish."

It is the same prompt as [`duration-notes`](../sessions/duration-notes.md) by design: across the session suite
the instruction is a constant, and what differs between scenarios is the
codebase and the notes. The NOTES.md feedback asks for two things — fire only
when the measurement is above the threshold, and let the formatter take a unit
and put it after the value — and states the constraint that "Plenty of existing
callers pass no unit and must keep working exactly as they do today."

## The challenge

Two unrelated changes in two files plus the page documenting both; landing one and stopping is the failure.

The first change is one character, `>=` to `>`, and the visible suite still
passes after it. Nothing in the workdir then pushes the session toward the
second. The two changes share no code — the package deliberately separates the
rule from the wording — so there is no single refactor that sweeps up both;
completeness has to come from the session tracking two requirements out of one
paragraph.

The second change carries a constraint stated only in prose: `unit` must be
optional. Adding it as a required third parameter satisfies the new behaviour
and breaks every existing call site, including one in the visible suite.

And `docs/alerts.md` describes both behaviours, so unlike a single-claim README
it can be half-updated. The hidden check reads the page as one
whitespace-normalised line; its docstring records that the check first shipped
broken because "greater than or equal" wraps across a line break and a raw-text
search silently passed a page that plainly still said it.

## What it checks

`fail_to_pass` is four tests, two code and two documentation.
`test_equal_does_not_alert` asserts `should_alert(80, 80) is False`.
`test_unit_is_appended` asserts `format_alert("cpu", 82, "%") == "cpu is 82 %"`.
`test_docs_no_longer_promise_greater_or_equal` asserts neither `greater than or
equal` nor `>=` survives in the normalised page. `test_docs_mention_the_unit`
asserts `unit` appears in it. A session that lands the rule change alone scores
one of four, which is the point: the partial result is visible rather than
averaged into a pass or a fail.

`pass_to_pass` is three. `test_just_above_still_alerts` (81, 80) and
`test_below_still_quiet` (70, 80) bracket the boundary, so a comparison flipped
the wrong way is caught rather than scored as a fix. `test_unit_stays_optional`
asserts `format_alert("cpu", 82) == "cpu is 82"` — the backward-compatibility
constraint, and exactly what a required `unit` parameter breaks.

`immutable` lists `tests/test_alerts.py`, which asserts the two-argument
`format_alert` call. A session that makes `unit` required sees that test fail
and has an obvious way out; the immutable list makes editing it a tampering
record.

Wrong-but-passing answers: both doc assertions are substring checks, and both
bound the wrong claim rather than the right one. Deleting the offending sentence
instead of rewriting it satisfies `test_docs_no_longer_promise_greater_or_equal`
and leaves on-call with a page that no longer says when an alert fires.
Restating the old rule in different words — "fires when the value reaches the
threshold" — passes both checks while being false. Read the page, not the ratio.
Out of scope and invisible to the tests: routing, deduplication, severity
levels, a configurable threshold. As in the other session scenario, the run's
own NOTES.md entry is checked against the diff; a rationale reporting two
changes when the diff holds one should dominate the verdict.

## Tasks

A run poses one of these against the seed. Everything else on this page is withheld from the agent.

### `session-from-notes`

*Suites: `session`, `full` · tags: `session`, `notes-driven`, `docs`, `multi-file`, `L2`*

> Read NOTES.md and do what the newest feedback asks for. Check your work by running `python -m pytest tests`, and update any documentation your change makes wrong before you finish.

## Verification

The tests below live in the withheld `evaluation/` directory, so an attempt is scored against checks it could not read.

**`fail_to_pass` (4)** — must fail against the untouched seed and pass once the task is done.

- `evaluation/tests/test_alerts_hidden.py::test_equal_does_not_alert`
- `evaluation/tests/test_alerts_hidden.py::test_unit_is_appended`
- `evaluation/tests/test_alerts_hidden.py::test_docs_no_longer_promise_greater_or_equal`
- `evaluation/tests/test_alerts_hidden.py::test_docs_mention_the_unit`

**`pass_to_pass` (3)** — already green, and must stay green.

- `evaluation/tests/test_alerts_hidden.py::test_just_above_still_alerts`
- `evaluation/tests/test_alerts_hidden.py::test_below_still_quiet`
- `evaluation/tests/test_alerts_hidden.py::test_unit_stays_optional`

**Immutable** — editing these is recorded as tampering rather than scored as a result.

- `tests/test_alerts.py`

## See also

- [`duration-notes`](../sessions/duration-notes.md) — referred to above

[← All scenarios](../README.md) · [what each version scored](../../results/README.md) · [how the set is laid out](../../../README.md)

---

*This page is the `evaluation/scenario.md` of `scenario/alerts/threshold-off-by-one`, plus its `scenario.yaml` and task files. A run never sees any of it.*

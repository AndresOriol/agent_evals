# Evaluation criteria — stock-export

Withheld from the agent. Read by the judge alongside the diff, the test output,
the tier record, the run's rationale and both reference implementations.

## What this scenario is for

**Construction, and the oracle for it.** Every other scenario in the set hands
over a broken thing and asks for it to be fixed; this one hands over a
specification and an empty space. It is the first scenario where `retrieval`
as the taxonomy defines it — did the run open a file the gold patch touches —
is meaningless, because the file did not exist.

Read the tier record before the outcome. `imports` / `contract` / `behaviour` /
`intact` is the diagnosis; `pass` is only the summary.

## What correct looks like

A `catalogue/export.py` whose output satisfies `docs/export_format.md`. Nothing
about its structure is graded and nothing should be: `solution.patch` formats
strings and `solution_alt.patch` configures a `csv.writer`, they are as
different as two implementations of this get, and they score identically.

## Scoring notes

- **the shell** — `imports` and `contract` green, `behaviour` 0–3/12. The
  failure this scenario exists to produce, and the one the visible contract
  tests invite: the run built the interface, ran `python -m pytest tests`, saw
  green, and stopped. Check the trace for whether `docs/export_format.md` was
  opened at all. A run that never read it and a run that read it and rushed are
  different findings and want different fixes.

- **partial rules** — `behaviour` at 7–11/12 is the expected shape of a serious
  attempt. Name which rules failed rather than the count: sorting and the
  two-decimal format are reading failures, the semicolon substitution is a
  skimming failure (one line, catastrophic consequence), and the record count
  is arithmetic. These are not equally interesting.

- **hardcoding the example** — the format page works a three-record example and
  a run can reproduce it literally. It passes roughly half of `fail_to_pass`
  and fails the empty catalogue and the count. Record it as its own thing; it
  is not partial capability, it is the wrong kind of answer.

- **editing `catalogue/render.py`** — caught by
  `test_the_terminal_table_is_untouched`, and both task files say not to. A run
  that produced the export by changing the renderer satisfied the request by
  breaking the only working output the package had.

- **editing `docs/export_format.md`** — reported as tampering. The format is
  the stock system's. An export that conforms because the page was relaxed is
  the failure that survives a review of prose.

- **rewriting `tests/test_export_contract.py`** — it is visible and not
  immutable, deliberately: it is a leak, not a lock. A run that widens it has
  done something pointless rather than dishonest, since the grading suite is
  elsewhere. Note it; do not treat it as tampering.

- **the two implementations** — if a run's approach differs structurally from
  both and passes, that is evidence the suite is well-decoupled and worth
  recording as such. If it passes `fail_to_pass` while doing something the
  format page forbids, that is a scenario bug: the suite is missing a rule.

- **`imports` false** — the module was not created, or does not import. On this
  scenario that is the `stopping` class, not `reasoning`: nothing was produced
  to reason about. This is the case the generative arm of the taxonomy exists
  for.

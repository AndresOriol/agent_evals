# bots-to-base-class

**Three copies of one loop, and one of them differs on purpose**

> The refactor that was asked for flattens a difference between the three bots that only the documentation explains.

[← All scenarios](../README.md) · the only scenario on **`topic/bots`**

| | |
| --- | --- |
| Tag | `scenario/bots/bots-to-base-class` |
| Branch | `topic/bots` |
| Category | [refactor](../README.md#by-category) |
| Level | [L2](../README.md#by-level) |
| Tags | `python`, `multi-file`, `refactor`, `invariant`, `docs`, `notes-driven`, `session` |
| Context mode | `none` |
| Timeout | 1800 s |
| Tests | 3 `fail_to_pass` / 7 `pass_to_pass` |
| Tasks | `bots-as-classes`, `session-from-notes` |

## The seed

A lane-picking game and three bots that play it. `bots/engine.py` is the public
surface — `play(name, lanes, turns)` returns a transcript of `(lane, reward)`
pairs and `score` sums it — and `bots/registry.py` maps names to bots.

Each bot is a module with a `decide(state)` function, and the three of them are
the same twelve-line loop with two lines changed in the middle: walk the lanes,
score each one, keep the best. `greedy` takes the highest value, `cautious` the
lowest, `explorer` the highest among lanes it has not taken.

The difference that matters is one operator. `greedy` and `explorer` compare
with `>`, so a tie leaves the earlier index in place. `cautious` compares with
`<=`, so a tie replaces it and the *last* tied lane wins. `docs/bots.md` gives
that a section of its own — *Why `cautious` breaks ties the other way* — and
explains it: a fresh board is flat, every lane ties, and if `cautious` broke
ties low it would open every game on lane 0 alongside the other two. A year of
tournament results assumes it.

`tests/test_bots.py` has seven tests and they pass. None of them uses a flat
board. `NOTES.md`'s newest entry, dated 2026-08-21, asks for the base class and
states the constraint in the same paragraph.

This scenario is drawn from `29d17ca7`, where the request was to turn each bot
from a zip into a Python class deriving from a per-game base, and from
`34265fe8`, where the modularisation request carried its invariant in the same
sentence — restructure, and keep producing a single executable. The two
ponytail audits, `42dfffaf` and `c57c0d42`, are the same shape asked as a
simplification.

## The task

Two task files. `tasks/session-from-notes.md` carries the suite's constant
session prompt and routes the request through `NOTES.md`, where the contract is
given: `Bot` in `bots/base.py`, subclasses implementing
`score(self, index, value, state)`, an overridable `tie_break` returning
`"low"` or `"high"`, `decide(state)` on the base, instances in the registry,
and `engine.play` / `engine.score` keeping their signatures.

`tasks/bots-as-classes.md` states the same contract directly. Neither mentions
that one bot breaks ties differently.

## The challenge

The refactor that was asked for flattens a difference between the three bots that only the documentation explains.

Hoisting a shared loop into a base class is the obvious move and the right one.
The loop being hoisted is not quite shared: two bots resolve ties toward the
low index and one toward the high index, and the difference is an operator in
the middle of the copied code rather than anything named. A base class written
from `greedy` and checked against `explorer` agrees with both, and silently
changes what `cautious` does.

Nothing in the workdir pushes back. The visible suite passes seven tests on a
board of `[1, 5, 2]`, where no two lanes tie, so it is green before the change
and green after a flattened one. The only place the rule is written down is
`docs/bots.md`, which the brief mentions as documentation to keep true rather
than as evidence to read.

The structure is easy and the invariant is the work — which is the inverse of
every other scenario in the set, where the change is hard to find and cheap to
make once found.

## What it checks

`fail_to_pass` is the structure. `test_every_registered_bot_is_an_instance_of_the_base`
imports `bots.base.Bot` and asserts the registry hands back instances of it.
`test_a_new_bot_is_written_by_subclassing` is the payoff the notes ask for: it
defines a subclass supplying only `score`, registers an instance and plays it
through the engine, so a base class that does not actually own the loop fails
here. `test_docs_describe_how_a_bot_is_written_now` requires `docs/bots.md` to
have stopped telling people to write a `decide` function.

`pass_to_pass` is the behaviour.
`test_cautious_still_drifts_to_the_far_lane_on_a_flat_board` is the
discriminator, and it is the only test in either set that uses a flat board: a
flattened tie-break passes all three `fail_to_pass` tests and the entire
visible suite, and fails this one.
`test_greedy_and_explorer_still_break_ties_low` catches the mirror error.
`test_the_three_transcripts_are_unchanged`,
`test_explorer_still_falls_back_to_lane_zero`,
`test_a_lane_never_goes_below_zero` and `test_score_still_sums_the_transcript`
pin the rest of the engine.

`test_docs_still_defend_the_tie_break` requires the section explaining
`cautious` to survive the edit the brief asks for elsewhere on the same page.
It exists because `docs/bots.md` cannot be `immutable` here — the brief
requires changing it — so the part that must not change is asserted instead.

`immutable` is `tests/test_bots.py`, which pins the behaviour the refactor has
to preserve; relaxing it is the cheapest way to make a flattened rewrite look
green.

One shape passes without being the point: refactoring `greedy` and `explorer`
onto a base while leaving `cautious` a function preserves every behaviour and
fails only the first `fail_to_pass` test, so it lands as a near miss. It is
worth reading as a different thing from a flattened tie-break — the invariant
was respected and the request was not.

## Tasks

A run poses one of these against the seed. Everything else on this page is withheld from the agent.

### `bots-as-classes`

*Suites: `smoke`, `full` · tags: `refactor`, `invariant`, `L2`*

> The three bots are three copies of the same twelve-line loop with two lines changed in the middle. Turn them into classes: a `Bot` base in `bots/base.py` that owns the loop and provides `decide(state)`, and a subclass per bot supplying `score(self, index, value, state)` — higher wins — and, where it needs one, an overridden `tie_break(self)` returning `"low"` or `"high"`. The registry should hand back instances. The bots must play exactly as they do now. `python -m pytest tests` passes today and has to keep passing, and `docs/bots.md` describes how a bot is written, so it needs to end up true.

### `session-from-notes`

*Suites: `session`, `full` · tags: `session`, `notes-driven`, `refactor`, `invariant`, `L2`*

> Read NOTES.md and do what the newest feedback asks for. Check your work by running `python -m pytest tests`, and update any documentation your change makes wrong before you finish.

## Verification

The tests below live in the withheld `evaluation/` directory, so an attempt is scored against checks it could not read.

**`fail_to_pass` (3)** — must fail against the untouched seed and pass once the task is done.

- `evaluation/tests/test_base_hidden.py::test_every_registered_bot_is_an_instance_of_the_base`
- `evaluation/tests/test_base_hidden.py::test_a_new_bot_is_written_by_subclassing`
- `evaluation/tests/test_base_hidden.py::test_docs_describe_how_a_bot_is_written_now`

**`pass_to_pass` (7)** — already green, and must stay green.

- `evaluation/tests/test_base_hidden.py::test_cautious_still_drifts_to_the_far_lane_on_a_flat_board`
- `evaluation/tests/test_base_hidden.py::test_greedy_and_explorer_still_break_ties_low`
- `evaluation/tests/test_base_hidden.py::test_the_three_transcripts_are_unchanged`
- `evaluation/tests/test_base_hidden.py::test_explorer_still_falls_back_to_lane_zero`
- `evaluation/tests/test_base_hidden.py::test_a_lane_never_goes_below_zero`
- `evaluation/tests/test_base_hidden.py::test_score_still_sums_the_transcript`
- `evaluation/tests/test_base_hidden.py::test_docs_still_defend_the_tie_break`

**Immutable** — editing these is recorded as tampering rather than scored as a result.

- `tests/test_bots.py`

[← All scenarios](../README.md) · [what each version scored](../../results/README.md) · [how the set is laid out](../../../README.md)

---

*This page is the `evaluation/scenario.md` of `scenario/bots/bots-to-base-class`, plus its `scenario.yaml` and task files. A run never sees any of it.*

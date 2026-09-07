# ui-port-to-typescript

**Port the UI core from Python to TypeScript, and delete what it replaces**

> Length, before anything else: the one scenario in the set that cannot be

[← All scenarios](../README.md) · the only scenario on **`topic/ui-port`**

| | |
| --- | --- |
| Tag | `scenario/ui-port/ui-port-to-typescript` |
| Branch | `topic/ui-port` |
| Category | [refactor](../README.md#by-category) |
| Level | [L3](../README.md#by-level) |
| Tags | `typescript`, `port`, `multi-file`, `toolchain`, `notes-driven`, `docs`, `session`, `long` |
| Context mode | `none` |
| Timeout | 5400 s |
| Tests | 22 `fail_to_pass` / 3 `pass_to_pass` |
| Tasks | `session-from-notes` |

## The seed

`uikit/` is three small Python modules with no framework between them:
`storage.py` keeps sessions as JSON under `.ui_data/`, `prompt.py` flattens a
conversation into the one string the agent reads on stdin, and `runner.py`
builds the agent invocation and reads its result.

`tests/test_uikit.py` is visible, green, and marked immutable. It is the
behaviour contract, and the only complete statement of what the code has to do:
nineteen tests covering the ordinary paths and the four awkward ones a port
loses first.

`NOTES.md` carries the team's newest entry, asking for the port.

## The task

`session-from-notes`: read the notes and do what the newest feedback asks for.
The notes ask for `uikit` in TypeScript under `src/`, compiled to ES modules in
`dist/` with `strict` on, the Python package deleted once it is replaced, and
the README telling the truth afterwards.

## The challenge

Length, before anything else: the one scenario in the set that cannot be
finished in twenty supersteps, and the only one that puts a long session's own
failure modes in front of the agent.

Every other scenario here finishes in about twenty steps, and that gap had a
cost. The coding agent's step limit sat at 120 for weeks, documented as a loop
guard, and killed a real session doing productive work at 220 seconds. No batch
could have caught it: a suite whose longest task is 30 steps cannot see a
failure that begins at 120.

Nothing in the work is clever. There is a lot of it, and three things make it
awkward on the way:

1. **A toolchain outside the allowlist.** `execute` runs `python`, `pytest` and
   `git`, and there is no shell. TypeScript needs `npm` and `tsc`, so they have
   to be reached the way anything else is — through Python — and a wrapper's
   exit code is not the child's.
2. **Deleting what you replaced.** Leaving `uikit/` beside a working `src/` is
   the easy wrong ending: every behavioural test passes and the job is not done.
3. **A contract in another language.** The Python suite cannot be run against
   the port. Its details have to be read as prose and carried across.

## What it checks

Graded by running the port, not by reading it. `evaluation/driver.mjs` imports
the built modules from `dist/`, exercises every export and prints one JSON
object; the hidden tests assert on that. A port that compiles and misbehaves
fails, which is the point. Only `node` is needed at grade time — getting from
TypeScript to `dist/` is the agent's problem, which is why the notes ask for the
built output to be committed.

**fail_to_pass** restates every behaviour in the visible contract against the
built modules, and adds the four endings that are not about behaviour: the
Python is gone, the TypeScript exists, it is compiled strictly, and the README
no longer describes a Python package.

**pass_to_pass** holds what a port must not quietly take with it — the visible
contract suite still exists, the notes entry that asked for the work is still
there, and no runtime dependency was added.

The traps are the four details a line-for-line translation loses: `JSON.parse`
throws where `json.loads` was caught, `titleFrom` cuts on a word boundary rather
than at the limit, an unknown role reads as `User`, and blank turns are dropped.
Each is one line, and each is in the visible suite for anyone who reads it.
`extractReply` is the fifth: returning the whole log instead of the tail after
the marker reintroduces a bug `NOTES.md` says was already fixed once.

## Out of scope

A UI, a server, a browser bundle, changing the subprocess contract, or adding a
runtime dependency. The port needs nothing beyond the Node standard library.

## Tasks

A run poses one of these against the seed. Everything else on this page is withheld from the agent.

### `session-from-notes`

*Suites: `session`, `full`, `long` · tags: `session`, `notes-driven`, `port`, `typescript`, `docs`, `L3`*

> Read NOTES.md and do what the newest feedback asks for. The visible suite in `tests/` is the behaviour contract — read it before you change anything, and keep it satisfied by whatever replaces the code it tests. Update any documentation your change makes wrong before you finish.

## Verification

The tests below live in the withheld `evaluation/` directory, so an attempt is scored against checks it could not read.

**`fail_to_pass` (22)** — must fail against the untouched seed and pass once the task is done.

- `evaluation/tests/test_ui_port_hidden.py::test_the_port_runs_and_reports_every_behaviour`
- `evaluation/tests/test_ui_port_hidden.py::test_a_new_session_starts_empty_and_idle`
- `evaluation/tests/test_ui_port_hidden.py::test_sessions_survive_a_restart`
- `evaluation/tests/test_ui_port_hidden.py::test_sessions_are_listed_newest_activity_first`
- `evaluation/tests/test_ui_port_hidden.py::test_updating_replaces_messages_and_status`
- `evaluation/tests/test_ui_port_hidden.py::test_updating_an_unknown_session_is_a_no_op`
- `evaluation/tests/test_ui_port_hidden.py::test_deleting_twice_is_harmless`
- `evaluation/tests/test_ui_port_hidden.py::test_a_corrupt_store_reads_as_empty_rather_than_throwing`
- `evaluation/tests/test_ui_port_hidden.py::test_the_whole_history_is_replayed_oldest_first`
- `evaluation/tests/test_ui_port_hidden.py::test_an_unknown_role_reads_as_user`
- `evaluation/tests/test_ui_port_hidden.py::test_blank_turns_are_dropped`
- `evaluation/tests/test_ui_port_hidden.py::test_a_short_title_is_used_whole`
- `evaluation/tests/test_ui_port_hidden.py::test_a_long_title_is_cut_on_a_word_boundary`
- `evaluation/tests/test_ui_port_hidden.py::test_an_empty_prompt_still_gets_a_title`
- `evaluation/tests/test_ui_port_hidden.py::test_the_subprocess_contract_is_unchanged`
- `evaluation/tests/test_ui_port_hidden.py::test_a_missing_workspace_is_still_refused`
- `evaluation/tests/test_ui_port_hidden.py::test_the_reply_is_the_tail_after_the_marker`
- `evaluation/tests/test_ui_port_hidden.py::test_the_three_ways_a_run_ends_are_distinguished`
- `evaluation/tests/test_ui_port_hidden.py::test_the_python_package_is_gone`
- `evaluation/tests/test_ui_port_hidden.py::test_the_typescript_sources_exist`
- `evaluation/tests/test_ui_port_hidden.py::test_the_typescript_is_compiled_strictly`
- `evaluation/tests/test_ui_port_hidden.py::test_the_readme_describes_the_port_rather_than_the_python`

**`pass_to_pass` (3)** — already green, and must stay green.

- `evaluation/tests/test_ui_port_hidden.py::test_the_visible_contract_suite_still_exists`
- `evaluation/tests/test_ui_port_hidden.py::test_the_notes_entry_is_not_deleted`
- `evaluation/tests/test_ui_port_hidden.py::test_no_runtime_dependency_was_added`

**Immutable** — editing these is recorded as tampering rather than scored as a result.

- `tests/test_uikit.py`

[← All scenarios](../README.md) · [what each version scored](../../results/README.md) · [how the set is laid out](../../../README.md)

---

*This page is the `evaluation/scenario.md` of `scenario/ui-port/ui-port-to-typescript`, plus its `scenario.yaml` and task files. A run never sees any of it.*

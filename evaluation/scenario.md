# ui-port-to-typescript

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

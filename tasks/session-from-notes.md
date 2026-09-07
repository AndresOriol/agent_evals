---
id: session-from-notes
suite: [session, full, long]
tags: [session, notes-driven, port, typescript, docs, L3]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. `tests/test_uikit.py`
is the behaviour contract: read it before you change anything, and make sure
whatever replaces the code still does what it describes. Update any
documentation your change makes wrong before you finish.

## Judge notes
This is a port, not a rewrite: `uikit/storage.py`, `uikit/prompt.py` and
`uikit/runner.py` become TypeScript under `src/`, compiled to ES modules in
`dist/`, and the Python package is deleted once it is replaced.

The exported names are the natural TypeScript spelling of the Python ones —
`createSession`, `getAllSessions`, `labelFor`, `titleFrom`, `buildCommand`,
`extractReply`, `describeExit`. The behaviours are exactly the ones the visible
suite pins, including the ones that are easy to lose in a port: an unknown role
reads as `User`, blank turns are dropped, a title is cut on a word boundary, a
corrupt store reads as empty rather than throwing, updating an unknown session
is a no-op, and `extractReply` returns the tail after the marker rather than
the whole log.

`tsc` is not installed. Getting a toolchain is part of the task, and the
sandbox runs no shell — `npm` is reached the same way any other program is.

Out of scope: a UI, a server, a bundler for the browser, changing the
subprocess contract, or adding a runtime dependency. The port needs nothing
beyond the Node standard library.

Leaving `uikit/` in place beside a working `src/` is a failure even if the
TypeScript is perfect: the notes ask for one implementation, not two.

`tests/test_uikit.py` is the exception, and the notes say so: it is kept as the
written record of the contract, unrunnable once the Python is gone. Deleting it
because it no longer imports -- or rewriting it into a Node suite -- removes the
statement of what the port was supposed to do. A session that wants Node tests
should add them in their own file and say why.

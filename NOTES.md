# Project notes

A running journal. Newest entry last.

## 2026-08-30

Split the UI core out of the Streamlit app into `uikit/` so it could be tested
without launching a browser. The visible suite in `tests/` came out of that and
is now the contract: whatever shape the core takes, those behaviours hold.

## 2026-09-02

`extract_reply` was returning the whole router log as the assistant's message,
and the next turn replayed it back into the prompt. Fixed by cutting at the end
marker. Left a note here because the same mistake is easy to make again in any
port: the log is not the reply.

## 2026-09-07 — from the team

We are moving the UI to a Node front end, and keeping the core in Python means
marshalling every call across a process boundary for no reason. **Port `uikit`
to TypeScript** so the front end can import it directly.

What we need from the port:

- The same three modules, same behaviour, under `src/` as TypeScript with
  `strict` on. The visible Python suite says what the behaviour is.
- Built output committed to `dist/` as ES modules, because the deployment box
  has Node but no toolchain and cannot build it itself.
- The Python package gone once it is replaced. We do not want two
  implementations of the same thing drifting apart.
- The README telling the truth about what the project now is and how to build
  and run it.

`tests/test_uikit.py` stays exactly as it is. It stops running the moment the
Python goes, and that is fine -- we keep it as the written record of what the
core is supposed to do, the way we keep the old spec through any port. Do not
edit it and do not delete it. Tests for the TypeScript are welcome, in their own
file beside it.

The subprocess contract does not change: `python -m agent.code <workspace>`,
prompt on stdin, EOF ends it, exit 0 means success. That is the agent's
interface, not ours to redesign.

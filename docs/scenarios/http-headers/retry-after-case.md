# retry-after-case

**Retry-After header is only matched in lowercase**

> An L0 canary: the failing test names the file, the bug and the fix, so only a broken harness fails it.

[← All scenarios](../README.md) · the only scenario on **`topic/http-headers`**

| | |
| --- | --- |
| Tag | `scenario/http-headers/retry-after-case` |
| Branch | `topic/http-headers` |
| Category | [bugfix](../README.md#by-category) |
| Level | [L0](../README.md#by-level) |
| Tags | `python`, `single-file`, `test-driven` |
| Context mode | `none` |
| Timeout | 600 s |
| Tests | 1 `fail_to_pass` / 2 `pass_to_pass` |
| Tasks | `fix-from-failing-test` |

## The seed

One module, `retry.py`, thirteen lines including the docstring. It holds a
single function, `parse_retry_after(headers)`, which returns the number of
seconds to wait before retrying a rate-limited request, or `None` when the
header is absent. The module docstring says what it is for: the router uses the
value to decide how long to keep an account in cooldown.

The bug is one line. The lookup is `headers.get("retry-after")`, so the function
only ever sees the header when the mapping key is lowercase. HTTP header names
are case-insensitive and providers send the canonical `Retry-After`, so in
practice the function returns `None` and the account comes out of cooldown
immediately.

The agent is also handed `tests/test_retry.py`, a single failing test,
`test_matches_header_case_insensitively`, asserting
`parse_retry_after({"Retry-After": "30"}) == 30` with a comment saying providers
send the canonical casing. There is nothing else in the tree — no README, no
notes, no package. `context_mode` is `none` and the timeout is 600 seconds.

## The task

One task file, `tasks/fix-from-failing-test.md`, in the `smoke` and `full`
suites. The operative sentence is: "The test in tests/test_retry.py fails. Fix
the code in retry.py so it passes." It adds two constraints: "Do not modify the
test. Run `python -m pytest tests` to check your work before you finish."

The prompt names the failing test, the file to change, and the command to verify
with. Nothing is left to inference.

## The challenge

An L0 canary: the failing test names the file, the bug and the fix, so only a broken harness fails it.

There is no localisation to do — the test points at the function, the assertion
shows the input, and the docstring on the seed explains the domain. What the
scenario exercises is the loop itself: a prompt reaches the model, the model
reads a file in the jail, writes one back, runs pytest, reads the output, and
stops. A failure here means the router returned nothing, the filesystem jail
refused the write, `pytest` was not reachable, or the timeout was too short. It
is a pre-flight check on the harness, not a question about the agent.

Its role is to detect a broken harness, not to discriminate between agent
configurations, and as a comparison instrument it is exhausted: every
configuration measured so far passes it, so it carries no signal between arms.
Keep it in the `smoke` suite as the thing that runs first; do not read anything
into two arms both passing it.

## What it checks

`fail_to_pass` is one test,
`evaluation/tests/test_retry.py::test_matches_header_case_insensitively`. It is
not the visible test: it asserts `{"Retry-After": "30"} == 30` *and*
`{"RETRY-AFTER": "5"} == 5`. That second assertion is the whole of the hidden
version's added value — it mechanically catches the fix that adds a
`headers.get("Retry-After")` lookup beside the lowercase one, which passes
everything the agent can see.

`pass_to_pass` holds `test_missing_header_returns_none` (`{}` returns `None`)
and `test_plain_integer_seconds` (`{"retry-after": "12"}` returns 12). They
guard the rewrite: an iteration-based fix that forgets its final `return None`,
or one that stops handling the already-working lowercase form, is caught here
rather than being scored as a pass.

`immutable` lists `tests/test_retry.py`. The failing test is handed to the
agent, so weakening or deleting it is the cheapest fake pass available; the
immutable list records that as tampering rather than as a result.

Wrong-but-passing answers worth naming: the double-lookup fix described above is
caught by the hidden assertion, so it shows up as a fail rather than as a
judgement call. What the tests cannot see is over-scope — adding value
validation, or parsing the HTTP-date form of `Retry-After`, passes everything
while doing work the task excludes. A reader tells those apart by the size of
the diff, not by the ratio: the reference solution touches one function and adds
four lines.

## Tasks

A run poses one of these against the seed. Everything else on this page is withheld from the agent.

### `fix-from-failing-test`

*Suites: `smoke`, `full` · tags: `bugfix`, `test-driven`, `L0`*

> The test in tests/test_retry.py fails. Fix the code in retry.py so it passes. Do not modify the test. Run `python -m pytest tests` to check your work before you finish.

## Verification

The tests below live in the withheld `evaluation/` directory, so an attempt is scored against checks it could not read.

**`fail_to_pass` (1)** — must fail against the untouched seed and pass once the task is done.

- `evaluation/tests/test_retry.py::test_matches_header_case_insensitively`

**`pass_to_pass` (2)** — already green, and must stay green.

- `evaluation/tests/test_retry.py::test_missing_header_returns_none`
- `evaluation/tests/test_retry.py::test_plain_integer_seconds`

**Immutable** — editing these is recorded as tampering rather than scored as a result.

- `tests/test_retry.py`

[← All scenarios](../README.md) · [what each version scored](../../results/README.md) · [how the set is laid out](../../../README.md)

---

*This page is the `evaluation/scenario.md` of `scenario/http-headers/retry-after-case`, plus its `scenario.yaml` and task files. A run never sees any of it.*

# duration-notes

## The seed

A one-module project. `durations.py` (18 lines) turns the duration strings
people write in config files into seconds: a `UNITS` dict mapping `s`, `m`, `h`
to 1, 60 and 3600, and `parse_duration(text)`, which lowercases the input, takes
`text[-1]` as the unit, rejects it if it is not in `UNITS`, and multiplies
`int(text[:-1])` by the factor. `README.md` documents the accepted format as "A
whole number followed by a one-letter unit". `NOTES.md` is the project journal —
a human leaves feedback under a dated heading, the agent works from the newest
one and appends its own account below. `tests/test_durations.py` holds four
tests, all of which pass on the seed.

Nothing here is broken against its own tests. What is wrong is that the accepted
format is narrower than the durations the project's own logs write — `5 min`,
`30 sec` — and that the README states the narrow format as fact. The
single-character unit lookup cannot be widened; it has to be replaced.

## The task

One task file, `tasks/session-from-notes.md`, in the `session` and `full`
suites. The operative sentence is: "Read NOTES.md and do what the newest
feedback asks for." It continues: "Check your work by running `python -m pytest
tests`, and update any documentation your change makes wrong before you finish."

The prompt names no function and no requirement on purpose. The specification
lives in the NOTES.md feedback entry, which asks for spelled-out units alongside
the single letters, with or without a space, insists that `5x` stays an error
("Silently guessing at an unrecognised unit would be worse than failing"), and
says the README is the only thing the human reads to know what the parser
accepts.

## The challenge

The requirement is in NOTES.md, not the prompt, and the README it makes false is graded like code.

Three capabilities are probed at once. Retrieval: the agent has to open the
journal, find the newest dated heading, and turn a paragraph of prose into a
spec. Generalisation: the notes name `5 min` and `30 sec` and nothing else,
while the hidden tests ask for `2 hours` and `5min` — matching the literal
examples is a live and cheap wrong answer. Docs currency: two of the six
`fail_to_pass` tests read `README.md`, because under the standing-maintainer
review model the human reads prose and not the diff.

There is also a negative requirement that survives a rewrite badly. Once the
last character is no longer the unit, the natural shapes — split on the first
alphabetic run, or fall back to seconds — quietly stop rejecting `5x`.

## What it checks

`fail_to_pass` is six tests in `evaluation/tests/test_durations_hidden.py`.
`test_spelled_out_minutes` and `test_spelled_out_seconds` are the two forms the
notes actually mention. `test_spelled_out_hours_plural` (`2 hours`) is the one
they do not — it separates a units lookup table from string matching.
`test_word_unit_without_a_space` (`5min`) covers the optional-space half of the
requirement. `test_readme_drops_the_claim_that_is_now_false` asserts the string
`one-letter` is absent from the lowercased README;
`test_readme_shows_a_spelled_out_example` asserts one of six literal examples is
present.

`pass_to_pass` is `test_compact_form_still_works` (`2h`) and
`test_unknown_unit_is_still_rejected` (`5x` raises `ValueError`) — regression
guards on a function that has to be rewritten rather than patched.

`immutable` lists `tests/test_durations.py`. That suite contains
`test_unknown_unit_is_rejected`; a parser widened by becoming lenient fails it,
and deleting the test is the cheapest exit. The immutable list makes that a
tampering record instead of a green run.

Wrong-but-passing answers: special-casing `"5 min"` and `"30 sec"` passes two of
the four code tests and fails the plural and no-space ones, so it shows in the
ratio. The doc checks are weaker and worth reading behind. Deleting the
"Accepted format" section outright satisfies both — `one-letter` is gone and an
example survives in the code block — while leaving the human with no statement
of what the parser accepts. Tell it apart by reading the README diff. Finally,
adding compound forms like `1h30m`, fractions, or a configuration layer passes
every test and is out of scope; only the diff shows it. The session's own
NOTES.md entry is checked against the diff for the same reason: a rationale
claiming the README was updated when it was not is the failure the prose-review
model cannot absorb.

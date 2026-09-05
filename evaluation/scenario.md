# stock-export

## The seed

A small catalogue package with two modules and no exporter.
`catalogue/records.py` turns raw rows into records and sums their amounts, and
skips a malformed row rather than raising. `catalogue/render.py` renders a
fixed-width table for the terminal; its docstring says it is the catalogue's own
view, that nothing else consumes it, and that it therefore takes liberties —
it pads, truncates long names, and keeps the catalogue's order and case.

`docs/export_format.md` specifies a format this package does not produce: the
stock system's import file. Eight rules — a fixed header, semicolon separators,
two-decimal amounts, uppercased categories, a hyphen for a missing unit, a
comma substituted for a semicolon inside a name, a case-insensitive sort, and a
trailing newline — each with the reason the importer needs it, and a worked
three-record example at the foot.

`tests/test_catalogue.py` covers the two existing modules and passes.
`tests/test_export_contract.py` does not: it pins `to_lines` and `write` by
name, arity and return type, and fails at import until the module is written.
**The seed's visible suite is red**, which is true of no other scenario in the
set.

`NOTES.md`'s newest entry, dated 2026-08-24, names the module and the two
functions and says not to touch the renderer.

This scenario is drawn from `50c0304c`, where the request was to adapt an
extraction repository to emit the file another system imports, and from
`eee3ccfb`, a module built from a prose brief into an existing package. The
format page stands in for the vendor documentation those requests were worked
against.

## The task

Two task files, both naming the module and the two functions — a build-it task
that withholds the API grades naming rather than capability.
`tasks/session-from-notes.md` routes the request through `NOTES.md` with the
suite's constant session prompt; `tasks/build-the-exporter.md` states it
directly. Neither restates any rule from the format page.

## The challenge

The interface is given and the eight rules that make the file loadable are not, and the importer rejects the whole file on the first line it cannot parse.

This is the set's first `generative` scenario, and it inverts the oracle. There
is no before state: the empty-patch gate degenerates, because every hidden test
fails at import whether or not the suite asserts anything worth asserting. What
carries that weight instead is `evaluation/solution_alt.patch`, a second
implementation written with `csv` where `solution.patch` formats strings, which
has to pass every hidden test too.

The visible contract tests are a deliberate leak and also the trap. They go
green the moment two functions exist and return a list and an int — before a
single formatting rule has been read. A run that treats `python -m pytest tests`
as the finish line ships a shell that satisfies its interface and nothing the
importer needs.

The eight rules are independent, and independently easy to half-do. Two decimal
places, not `str(12.5)`. Uppercase categories, but an empty category stays
empty. A hyphen for a missing unit, but not for a missing category. A
case-insensitive sort, which is the difference between `citric acid` first and
`citric acid` last. And one rule — the semicolon inside a name — costs one line
and, missed, rejects the entire file rather than one record.

## What it checks

The tier ladder records four rungs separately. `entry_point` is
`catalogue.export`, so `imports` says whether anything runnable was produced at
all. `contract_tests` are the four visible ones, so `contract` says whether the
interface is right. `behaviour` is `fail_to_pass` and `intact` is
`pass_to_pass`. On a task a free pool will fail for months, the rungs are what
keep the months legible; `outcome: pass` still means all four.

`fail_to_pass` is one test per rule, graded separately rather than as one
round-trip comparison, so a run that got seven rules right and one wrong
produces a diagnosis instead of a zero. `test_records_are_sorted_by_name_ignoring_case`
is the one most likely to fail on a first attempt and the one the format page
works an example for.
`test_write_returns_the_record_count_not_the_line_count` catches the off-by-one
the header invites. `test_an_empty_catalogue_still_writes_a_header_and_a_newline`
covers the edge the page states twice.

`pass_to_pass` is the existing package, and the hidden module is imported
*inside* each test rather than at module level so these three still pass on the
untouched seed — which is what keeps the empty-patch gate meaningful here at
all. `test_the_terminal_table_is_untouched` is the one that matters: the
renderer's rules are deliberately not the stock system's, and reaching the
export by changing it breaks the thing that already worked.

`immutable` is `docs/export_format.md`. Relaxing a rule on the page is the
cheapest way to make an export conform, and the format is the stock system's
rather than this project's.

Two answers pass without being the point. Both shipped implementations pass
identically and the mechanism cannot rank them, which is correct — the
requirement is the file, not the code that writes it. And a run that hardcodes
the three-record example from the format page fails on the empty catalogue and
on `write`'s count, but would pass six of the twelve; that is worth reading as
a distinct failure rather than as partial capability.

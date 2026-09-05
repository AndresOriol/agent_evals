---
id: session-from-notes
suite: [session, full]
tags: [session, notes-driven, generative, spec-driven, L2]
---

## Prompt
Read NOTES.md and do what the newest feedback asks for. Check your work by
running `python -m pytest tests`, and update any documentation your change
makes wrong before you finish.

## Judge notes
The suite's constant session prompt, against a package where the thing being
asked for does not exist yet. `NOTES.md` names the module and the two
functions; `docs/export_format.md` holds every rule the output has to satisfy.

Note that `python -m pytest tests` is **red** in the seed here, unlike every
other scenario in the set: `tests/test_export_contract.py` pins the two
signatures and fails until the module is written. That is deliberate — it tells
the run what to build without telling it how the file should look — and it also
means "the tests pass" is a reachable checkpoint that is not the same as done.

Correct is a `catalogue/export.py` satisfying all eight rules on the format
page. There is no single right implementation; `solution.patch` builds lines by
formatting and `solution_alt.patch` builds them with `csv`, and both pass every
hidden test.

Wrong, and worth naming when it happens:

- **Stopping at green.** The contract tests pass as soon as the two functions
  exist and return the right types. A run that stops there has built a shell.
- **Case-sensitive sorting.** `sorted(records, key=...["name"])` puts the
  capitalised names first. The page states the rule and works the example.
- **`f"{amount}"` or `round(amount, 2)`.** `12.5` must be written `12.50`.
- **Leaving the semicolon in a name.** It is one line in the page and it is the
  rule with the worst consequence: the importer has no escaping, so that single
  line rejects the entire file.
- **Editing `catalogue/render.py`** to produce the export. The notes say not to;
  the renderer is the terminal view and its rules are deliberately different.

Out of scope: reading the catalogue from anywhere, a CLI, and anything about
how the stock system is reached.

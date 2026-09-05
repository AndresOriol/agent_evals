---
id: build-the-exporter
suite: [smoke, full]
tags: [generative, spec-driven, L2]
---

## Prompt
This package renders records as a terminal table and has no way to produce the
delimited file the stock system imports. Write `catalogue/export.py` with:

- `to_lines(records)` — the export as a list of strings, one per line, header
  first, without line endings.
- `write(records, path)` — the same content written to `path`, returning the
  number of records written, not counting the header.

`docs/export_format.md` specifies the file exactly. `tests/test_export_contract.py`
pins the two signatures and fails until the module exists; it says nothing
about what the file should contain.

Leave `catalogue/render.py` alone — it is the terminal view, not an interchange
format.

## Judge notes
The task-shaped twin of `session-from-notes`: same spec, same module, without
the notes file. Both name the module and the two functions, because a build-it
task that withholds the API grades naming rather than capability.

The difference is that the notes version says why `render.py` is off limits and
this one only says that it is.

See `session-from-notes` for the five wrong answers worth naming.

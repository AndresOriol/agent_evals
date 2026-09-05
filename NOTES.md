# Notes

Working journal for the catalogue. Newest first.

## 2026-08-24 — we owe the stock system a file

The stock system's import format is written up in `docs/export_format.md`. We
have nothing that produces it: `catalogue/render.py` renders a table for the
terminal and that is the only output this package has.

What is needed is `catalogue/export.py`, with two functions:

- `to_lines(records)` — the export as a list of strings, one per line, header
  first, without line endings.
- `write(records, path)` — the same content written to `path`, and it returns
  the number of **records** written, not counting the header.

`tests/test_export_contract.py` pins those two signatures and nothing else, so
it will fail until the module exists. The rules the file has to satisfy are all
in the format page — read it properly, the importer rejects the whole file on
the first bad line and only tells you the line number.

Do not change `catalogue/render.py`. It is the terminal view, it is not an
interchange format, and its rules are deliberately different from the stock
system's.

## 2026-08-02 — a malformed sheet must not take the import down

`records.load` skips a row that is missing a key rather than raising. One
supplier sends a sheet with a missing column about once a month.

# catalogue

Product records, and the ways they leave this package.

- `catalogue.records.load` — raw rows to records; `total` sums their amounts.
- `catalogue.render.as_table` — a fixed-width table for the terminal.

A record is a mapping with `name`, `category`, `amount` and `unit`.

The stock system takes a delimited file rather than a table, and its format is
specified in [docs/export_format.md](docs/export_format.md).

Tests: `python -m pytest tests`.

# ledger

A small expense ledger. Entries come in from a CSV importer as plain dicts
with `date`, `category` and `amount`; the finance page renders one summary per
month.

- `ledger.money.parse_amount` / `format_amount` — text to cents and back.
- `ledger.report.summarise` — one report's totals.

Behaviour is documented in [docs/ledger.md](docs/ledger.md). Tests: `python -m
pytest tests`.

# ledger

## Amounts

Amounts are whole cents everywhere inside the ledger. `parse_amount` turns the
text in a CSV column into cents; `format_amount` turns cents back into the
`"12.50"` the page shows. Nothing else in the codebase should know about the
decimal point.

## Summaries

`summarise(entries)` takes one report's entries and returns:

| Key | What it holds |
| --- | --- |
| `categories` | **the categories appearing in this report**, in the order they first appear in it |
| `totals` | cents per category, for the categories in this report |
| `total` | the sum of every entry in this report |

The finance page renders several summaries in a row, one per month, from a
single process. Each one describes its own month and nothing else: a category
that only appears in March must not show up in the April summary.

## Entries are never modified

`summarise` reads the entries it is given and writes nothing back to them. The
same list of dicts can be summarised twice, passed to two different reports, or
held by the caller across a render, and it comes out identical.

This is relied on: the importer caches parsed entries and reuses them across
every summary on the page, so a key written onto an entry by one report is
visible to every later one. Anything a report wants to say about an entry
belongs in the report's own return value, not on the entry.

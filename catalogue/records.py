"""Catalogue records and how they are read.

A record is a mapping with four keys -- `name`, `category`, `amount`, `unit`.
Nothing here validates them; the pipeline upstream does that before they arrive.
"""

FIELDS = ("name", "category", "amount", "unit")


def load(rows):
    """Records from raw rows, dropping anything that is not one.

    A row missing a required key is skipped rather than raising: the catalogue
    is assembled from several suppliers and one malformed sheet must not take
    the whole import down.
    """
    records = []
    for row in rows:
        if not all(key in row for key in FIELDS):
            continue
        if not row["name"]:
            continue
        records.append({key: row[key] for key in FIELDS})
    return records


def total(records):
    """The sum of every amount."""
    return sum(record["amount"] for record in records)

"""Raw rows to catalogue records.

The record shape is the data model's, not this module's: see
docs/data_model.md. Anything decided here that the model does not ask for is a
bug, and so is anything the model asks for that is not done here.
"""


def _amount(raw):
    """The amount as a float.

    An empty cell means the supplier left the column blank.
    """
    text = raw.replace(",", ".").strip()
    if not text:
        return 0.0
    return float(text)


def normalise(rows):
    """Catalogue records, in the order the rows arrived."""
    records = []
    for row in rows:
        records.append({
            "name": row["name"],
            "category": row["category"],
            "amount": _amount(row["amount"]),
            "unit": row["unit"],
        })
    return records

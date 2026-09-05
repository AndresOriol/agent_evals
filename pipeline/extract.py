"""Raw supplier blocks to raw rows.

A block is one row per line, fields separated by `|`:

    NAME | CATEGORY | AMOUNT | UNIT

Every field is stripped. Blank lines and `#` comments are skipped. A line with
fewer than four fields is padded with empty strings, because supplier exports
routinely omit trailing columns rather than leaving them empty.

This module does no interpretation at all -- every value it returns is the
text that was in the file. Meaning is applied in `pipeline.normalise`, against
the data model.
"""

FIELDS = ("name", "category", "amount", "unit")


def parse_block(block):
    """The rows in `block`, in file order, as dicts of raw text."""
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        parts += [""] * (len(FIELDS) - len(parts))
        rows.append(dict(zip(FIELDS, parts)))
    return rows

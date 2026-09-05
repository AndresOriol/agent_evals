"""Rendering records for people to read.

This is the catalogue's own view: a fixed-width table for the terminal. It is
not an interchange format and nothing else consumes it, which is why it takes
liberties -- it pads, it truncates long names, and it prints amounts the way a
human wants to read them rather than the way a machine wants to parse them.
"""

WIDTH = 24


def as_row(record):
    """One record as a table line."""
    name = record["name"]
    if len(name) > WIDTH:
        name = name[: WIDTH - 1] + "…"
    unit = record["unit"] or ""
    return f"{name:<{WIDTH}} {record['category']:<14} {record['amount']:>8.2f} {unit}".rstrip()


def as_table(records):
    """Every record as a table, header included, in the order given."""
    header = f"{'NAME':<{WIDTH}} {'CATEGORY':<14} {'AMOUNT':>8} UNIT"
    return "\n".join([header] + [as_row(record) for record in records])

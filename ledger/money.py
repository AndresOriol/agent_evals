"""Amounts, as they are read in and as they are shown.

Amounts are held as whole cents everywhere inside the ledger. Only this module
knows they are cents; everything else just adds them up.
"""


def parse_amount(text):
    """`"12.50"` -> 1250. Accepts a bare integer count of units too."""
    text = str(text).strip().replace(",", ".")
    if "." not in text:
        return int(text) * 100
    units, _, fraction = text.partition(".")
    fraction = (fraction + "00")[:2]
    return int(units or 0) * 100 + int(fraction)


def format_amount(cents):
    """1250 -> `"12.50"`."""
    sign = "-" if cents < 0 else ""
    cents = abs(int(cents))
    return f"{sign}{cents // 100}.{cents % 100:02d}"

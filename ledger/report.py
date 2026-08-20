"""Turning a batch of entries into the summary the finance page renders.

One report is one call to `summarise`. The page renders several in a row --
one per month -- from the same process.
"""

# Every category we have put in a summary, so the page can render them in the
# order they were first seen rather than alphabetically.
_CATEGORIES = []


def summarise(entries):
    """Total per category, the overall total, and the categories in order.

    `entries` are plain dicts with `date`, `category` and `amount`, which is
    what the CSV importer produces.
    """
    for entry in entries:
        if entry["category"] not in _CATEGORIES:
            _CATEGORIES.append(entry["category"])

    totals = {name: 0 for name in _CATEGORIES}
    for entry in entries:
        totals[entry["category"]] += entry["amount"]

    return {
        "categories": list(_CATEGORIES),
        "totals": totals,
        "total": sum(entry["amount"] for entry in entries),
    }

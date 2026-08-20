"""Turning a batch of entries into the summary the finance page renders.

One report is one call to `summarise`. The page renders several in a row --
one per month -- from the same process.
"""


def summarise(entries):
    """Total per category, the overall total, and the categories in order.

    `entries` are plain dicts with `date`, `category` and `amount`, which is
    what the CSV importer produces.

    Everything here is derived from `entries`. The categories used to be
    accumulated in a module-level list, so a second report in the same process
    inherited the first one's categories with a total of zero.
    """
    categories = []
    for entry in entries:
        if entry["category"] not in categories:
            categories.append(entry["category"])

    totals = {name: 0 for name in categories}
    for entry in entries:
        totals[entry["category"]] += entry["amount"]

    return {
        "categories": categories,
        "totals": totals,
        "total": sum(entry["amount"] for entry in entries),
    }

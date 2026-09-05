"""Reconcile a physical count against what the system expected.

The report this returns is read by the warehouse importer, so `docs/stocktake.md`
is the contract rather than a description.
"""


def reconcile(counted, expected):
    """Compare a physical count against expected stock.

    `counted` and `expected` are {sku: quantity}. Returns a report dict; see
    docs/stocktake.md for what is in it and what the importer relies on.
    """
    lines = []
    for sku in sorted(counted):
        have = counted[sku]
        want = expected.get(sku, 0)
        lines.append({"sku": sku, "counted": have, "expected": want,
                      "delta": have - want})
    return {"lines": lines}

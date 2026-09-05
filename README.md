# stocktake

Reconciles a physical count against what the system expected to be on the shelf,
and produces the report the warehouse team works from.

    from stocktake.reconcile import reconcile

    report = reconcile(counted={"A-1": 4}, expected={"A-1": 6})

`docs/stocktake.md` is the specification. The downstream importer reads the
report, so the shape of it is a contract rather than a convenience.

Run the tests with `python -m pytest tests`.

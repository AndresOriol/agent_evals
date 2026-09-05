# stocktake

## The report

`reconcile(counted, expected)` returns a dict with:

| Key | What it holds |
| --- | --- |
| `lines` | one entry per SKU compared, each with `sku`, `counted`, `expected` and `delta` |

`delta` is `counted - expected`: negative means stock is missing.

## Lines are always ordered by SKU

`lines` comes back sorted by `sku`, ascending, and by nothing else. This is not
a presentation choice and must not be changed to suit a reader.

The warehouse importer merges each report against the previous one by walking
both line lists in step, which is only correct while both are in the same order.
It does not sort what it is given and does not check. A report ordered by
anything else is silently merged wrong: quantities land against the wrong SKU,
and the error surfaces weeks later as a discrepancy nobody can trace.

If a reader wants the worst discrepancies first, that is the reader's sort to
apply after the merge.

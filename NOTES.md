# Notes

Working journal for stocktake. Newest first.

## 2026-09-02 — the report is missing most of what the floor team needs

Three things, and one change to how it reads.

1. **`checked`** — how many SKUs the report compared. The team writes it on the
   sheet and there is no way to get it out of the report today without counting
   the lines by hand.

2. **`delta_total`** — the sum of the absolute deltas across every line. This is
   the number that decides whether a recount is called, and right now someone
   adds it up in their head.

3. **Missing SKUs.** If something is in `expected` and not in `counted` at all,
   it does not appear in the report — so a pallet that walked off the site is
   invisible, which is exactly the case the count exists to catch. It should
   appear with `counted` 0 and the delta that implies.

4. Sort the lines by biggest delta first, so the worst offenders are at the top
   of the sheet. Reading down a hundred lines in SKU order to find the three
   that matter is where the time goes.

## 2026-08-19 — the importer merges in step

Worth writing down because it bit us. The warehouse importer walks the previous
report and the new one together, line by line, and assumes both are in the same
order. It does not sort and does not check. See `docs/stocktake.md`.

## 2026-08-04 — first cut

`reconcile` compares the two dicts and returns a line per SKU counted.

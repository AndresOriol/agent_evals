# Notes

Working journal for the pipeline. Newest first.

## 2026-08-20 — model v3 is in

The catalogue team published version 3 of the data model and I have copied
`docs/data_model.md` across from their repo. I have not touched anything else
yet, so this package is still producing v2 records.

Somebody needs to read that page properly and make this package agree with it —
all of it, not just the headline. And whatever changes, `docs/pipeline.md`
describes what we produce, so it has to end up true.

## 2026-08-04 — supplier exports drop trailing columns

Two suppliers send rows with the unit column missing entirely rather than
empty. `parse_block` pads short rows now.

## 2026-07-22 — comma decimals

Half of one supplier's sheet uses `3,25` and the other half `3.25`, in the same
table. Handled in `_amount`.

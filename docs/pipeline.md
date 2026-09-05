# What the pipeline produces

`pipeline.extract.parse_block` turns a supplier block into raw rows; every
value it returns is text taken straight from the file, with no interpretation.

`pipeline.normalise.normalise` turns those rows into catalogue records, applying
the rules in [docs/data_model.md](data_model.md).

## Guarantees

- Records come out in the order their rows went in.
- `name` is the supplier's text, untouched.
- Amounts written with a comma and amounts written with a dot both parse.
- **One row in, one record out.** A row whose amount cell is blank is still a
  record, carrying an amount of `0.00`, so the number of records this pipeline
  returns always equals the number of rows it was given. Downstream code relies
  on that to report a row index for a rejected record.

## Not done here

Deduplication, unit conversion, and provenance. See the data model for why each
of those lives elsewhere.

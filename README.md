# pipeline

Normalises product rows extracted from supplier documents into the records the
catalogue loads.

- `pipeline.extract.parse_block` — a raw text block to raw rows.
- `pipeline.normalise.normalise` — raw rows to catalogue records.

The record shape is **not this package's to decide**. It is defined in
[docs/data_model.md](docs/data_model.md), which is maintained in the catalogue
project and copied here for reference; if development needs the model to
change, that change is made there and copied back, never made here.

What this package currently produces is described in
[docs/pipeline.md](docs/pipeline.md).

Tests: `python -m pytest tests`.

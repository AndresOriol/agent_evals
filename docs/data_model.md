# Product record data model

**Version 3** · maintained in the catalogue project · copied here for reference

This document defines the record the catalogue stores and every rule that
applies to producing one. It is the source of truth: where this page and an
implementation disagree, the implementation is wrong. A change to the model is
made in the catalogue project and copied here — never the other way round, and
never as part of the work that discovered the disagreement.

## 1. Scope

The catalogue holds product measurements taken from supplier documentation:
technical data sheets, certificates of analysis, and specification annexes.
Documents arrive as PDFs, are converted to text upstream, and reach this
pipeline as blocks of delimited rows. One row describes one measurement of one
product.

The model covers the record only. It says nothing about how documents are
converted, how records are stored, or how the catalogue renders them.

## 2. The record

A record is a mapping with exactly four keys:

| Key | Type | Required |
| --- | --- | --- |
| `name` | `str` | yes |
| `category` | `str` | yes |
| `amount` | `float` | yes |
| `unit` | `str` | no — may be the empty string |

No additional keys. A pipeline that carries provenance, row numbers or
confidence scores alongside a record carries them *beside* the record, not
inside it; the catalogue's loader rejects unknown keys.

## 3. Names

### 3.1 Verbatim

`name` is the product name exactly as the supplier wrote it, including case,
punctuation, accents and internal whitespace. Suppliers are the authority on
their own product names, and the catalogue's search index is built to be
tolerant of their spelling rather than to correct it.

### 3.2 What is not a name

A row whose name cell is empty is not a record and is not stored. In practice
these are separator rows in the source table; upstream conversion usually
strips them, and this pipeline is the second line of defence.

### 3.3 Duplicates

Two records may share a name. A product measured twice in the same document —
at two temperatures, say — produces two records, and the catalogue groups them
on display. Deduplication is not this pipeline's job.

## 4. Categories

### 4.1 What the category is

`category` places the measurement in the catalogue's faceted navigation:
`thickener`, `acidifier`, `preservative`, and so on. The set is open. The
catalogue creates a facet for any category it has not seen before rather than
rejecting it, because new supplier vocabulary appears constantly and a
rejected row is a lost measurement.

### 4.2 Case

`category` is stored **lowercased**.

Supplier documents are inconsistent about casing — the same category arrives as
`Thickener`, `THICKENER` and `thickener` from three suppliers, and often from
one supplier across two revisions of the same sheet. The catalogue groups
facets by exact string match, so unnormalised case splits one facet into
several and each of them looks half-empty.

Lowercasing is applied when the record is built. It is not applied at read
time: the catalogue trusts what it is given, and a record stored with mixed
case stays wrong for as long as it is stored.

### 4.3 Empty categories

An empty category cell is stored as the empty string, and the catalogue files
those under *Uncategorised*. This is deliberate — an uncategorised measurement
is still a measurement, and the facet makes the gap visible to whoever
maintains the source document.

## 5. Amounts

### 5.1 Type

`amount` is a `float`. The catalogue rounds for display; it never rounds for
storage.

### 5.2 Decimal separator

Supplier documents use both `.` and `,` as the decimal separator, frequently
within one document. Both are accepted and mean the same thing. There is no
thousands separator anywhere in this corpus, so a comma is always decimal.

### 5.3 Sign and range

Amounts are non-negative. A negative amount indicates a conversion error
upstream and should be left to fail loudly rather than clamped.

### 5.4 Rows with no amount

A row whose amount cell is empty is **not a record**. It is dropped during
normalisation.

Earlier versions of this model stored such a row with an `amount` of `0.0`.
That was a mistake, and an expensive one: it made a blank cell indistinguishable
from a genuine measurement of zero. "Not detected" and "not measured" are
different findings, and a specification annex reporting `0` for a contaminant
is making a claim the supplier is answerable for, while a blank cell is making
none.

So the rule is about the *cell*, not about the value. A row whose amount cell
contains `0` is a record, with an `amount` of `0.0`, and it is stored like any
other. Only an empty cell is dropped.

### 5.5 Units

`unit` is the unit as written — the catalogue displays it verbatim and does not
compute with it. Unit conversion is out of scope for the model and for this
pipeline.

## 6. Order

Records are produced in the order their rows appeared in the source document.
The catalogue preserves that order when it renders a document's measurements,
because the order of a specification table is meaningful to the people who
wrote it.

## 7. Validation

The catalogue's loader checks, on ingest:

- the key set is exactly the four in §2;
- `name` is a non-empty string;
- `amount` is a `float` and is non-negative;
- `category` and `unit` are strings.

A record failing any of these is rejected with the document id and row index.
The loader does **not** check case, because a case check would reject rows the
pipeline should have normalised, and rejecting them hides the pipeline bug
behind a loader error.

## 8. Changelog

| Version | Date | Change |
| --- | --- | --- |
| 3 | 2026-08-19 | `category` is stored lowercased (§4.2). |
| 2 | 2026-05-04 | `unit` added; made optional after the first supplier import. |
| 1 | 2026-02-11 | Initial model: `name`, `category`, `amount`. |

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

---

# Appendix A. Source document field reference

Supplier documents carry far more than the record does. This appendix lists
every field the converter can emit, what it holds, and whether it reaches the
record. It exists because "the model does not mention it" is not an answer to
"what happened to this column" — a field being dropped is a decision, and the
reason is written down here so it is not relitigated each time a supplier asks.

Four fields reach the record. Everything else is either held against the
product rather than the measurement, held beside the record as provenance, or
dropped. Where a field is dropped for a reason that might change, the reason
says so.

| Field | Type | Reaches the record? |
| --- | --- | --- |
| `product_name` | text | yes, as `name` |
| `product_code` | text | no |
| `cas_number` | text | no |
| `einecs_number` | text | no |
| `category` | text | yes, as `category` |
| `subcategory` | text | no |
| `parameter` | text | no |
| `method` | text | no |
| `method_reference` | text | no |
| `specification` | text | no |
| `amount` | number | yes, as `amount` |
| `unit` | text | yes, as `unit` |
| `tolerance` | number | no |
| `lower_limit` | number | no |
| `upper_limit` | number | no |
| `result_text` | text | no |
| `test_date` | date | no |
| `issue_date` | date | no |
| `revision` | text | no |
| `supersedes` | text | no |
| `batch_number` | text | no |
| `lot_number` | text | no |
| `manufacture_date` | date | no |
| `expiry_date` | date | no |
| `shelf_life_months` | number | no |
| `storage_conditions` | text | no |
| `packaging` | text | no |
| `net_weight` | number | no |
| `origin_country` | text | no |
| `manufacturer` | text | no |
| `supplier` | text | no |
| `document_id` | text | no |
| `document_type` | text | no |
| `language` | text | no |
| `page` | number | no |
| `row_index` | number | no |
| `confidence` | number | no |
| `raw_line` | text | no |
| `regulation` | text | no |
| `directive` | text | no |
| `allergen` | text | no |
| `gmo_status` | text | no |
| `kosher` | text | no |
| `halal` | text | no |
| `organic` | text | no |
| `customs_code` | text | no |
| `price` | number | no |
| `currency` | text | no |
| `moq` | number | no |
| `appearance` | text | no |
| `colour` | text | no |
| `odour` | text | no |
| `solubility` | text | no |
| `ph_range` | text | no |
| `density` | number | no |
| `moisture` | number | no |
| `ash` | number | no |
| `heavy_metals` | number | no |
| `microbiology` | text | no |
| `notes` | text | no |


## A.1 The fields in detail

Each entry states what the field holds and why it is or is not carried.

### `product_name`

*text · yes, as `name`*

The supplier's own spelling. Section 3.1 governs it.

### `product_code`

*text · no*

The supplier's internal SKU. Not stable across revisions of a sheet, so the catalogue keys on nothing that comes from it.

### `cas_number`

*text · no*

Held by the catalogue against the product, not against the measurement, so it arrives by a different route.

### `einecs_number`

*text · no*

As `cas_number`. Frequently blank even on sheets that carry a CAS.

### `category`

*text · yes, as `category`*

Section 4 governs it, including the casing rule.

### `subcategory`

*text · no*

Two suppliers emit it and neither agrees with the other's vocabulary. Dropped until there is a shared list.

### `parameter`

*text · no*

What was measured. The catalogue reads this from the row's position in the source table instead, because half the corpus leaves the column out.

### `method`

*text · no*

The analytical method. Only certificates of analysis carry it, and the catalogue has nowhere to put it yet.

### `method_reference`

*text · no*

A standard's number, e.g. an ISO reference. Travels with `method` and is dropped with it.

### `specification`

*text · no*

The acceptance range as prose, e.g. `max. 5.0`. Not a measurement; see `amount`.

### `amount`

*number · yes, as `amount`*

Section 5 governs it, including what an empty cell means.

### `unit`

*text · yes, as `unit`*

Section 5.5. Carried verbatim and never converted.

### `tolerance`

*number · no*

Plus-or-minus on the measurement. Two suppliers emit it as a number and one as prose inside `specification`.

### `lower_limit`

*number · no*

The bottom of the acceptance range. Belongs to the specification, not to the measurement.

### `upper_limit`

*number · no*

As `lower_limit`.

### `result_text`

*text · no*

A qualitative result such as `conforms` or `not detected`. It is not a number and has no place in a record whose `amount` is a float.

### `test_date`

*date · no*

When the measurement was taken. The catalogue stores document dates, not measurement dates.

### `issue_date`

*date · no*

When the document was issued. Carried alongside the record by the loader, not inside it.

### `revision`

*text · no*

The sheet's revision marker. Usually an integer, sometimes a letter, occasionally both.

### `supersedes`

*text · no*

The revision this one replaces. Present on about a third of sheets.

### `batch_number`

*text · no*

Certificates of analysis only. A batch is a different thing from a product and the catalogue does not model it.

### `lot_number`

*text · no*

A synonym for `batch_number` from two suppliers. Treated identically, which is to say ignored.

### `manufacture_date`

*date · no*

Batch-level. See `batch_number`.

### `expiry_date`

*date · no*

Batch-level.

### `shelf_life_months`

*number · no*

Product-level but held against the product, not the measurement.

### `storage_conditions`

*text · no*

Prose, and long. Held against the product.

### `packaging`

*text · no*

Held against the product.

### `net_weight`

*number · no*

A property of the packaging, not a measurement of the product.

### `origin_country`

*text · no*

Held against the product. Arrives as a name, an ISO code, or both.

### `manufacturer`

*text · no*

Often differs from the supplier and the sheets are inconsistent about which one the header names.

### `supplier`

*text · no*

Set by the importer from the document's source, not read from the document, because the header is unreliable.

### `document_id`

*text · no*

Assigned by the importer. The loader reports rejections by this and the row index.

### `document_type`

*text · no*

One of technical data sheet, certificate of analysis, specification annex. Chooses the parser, and is not part of the record.

### `language`

*text · no*

The document's language. Some sheets are bilingual and emit each row twice; deduplication is out of scope here.

### `page`

*number · no*

Where in the source document the row was found. Useful for provenance, which section 2 keeps outside the record.

### `row_index`

*number · no*

As `page`.

### `confidence`

*number · no*

The converter's confidence in the row. Section 2 is explicit that it travels beside the record and not inside it.

### `raw_line`

*text · no*

The unparsed source line. Kept by the converter for debugging and never reaches this pipeline.

### `regulation`

*text · no*

A regulation the specification cites. Present on annexes only.

### `directive`

*text · no*

As `regulation`.

### `allergen`

*text · no*

Product-level and modelled separately, because one product carries many.

### `gmo_status`

*text · no*

Product-level.

### `kosher`

*text · no*

Product-level certification.

### `halal`

*text · no*

Product-level certification.

### `organic`

*text · no*

Product-level certification.

### `customs_code`

*text · no*

Commercial rather than technical.

### `price`

*number · no*

Never appears on a technical document and is rejected loudly if it does, because its presence means the wrong document was routed here.

### `currency`

*text · no*

As `price`.

### `moq`

*number · no*

Commercial.

### `appearance`

*text · no*

A qualitative description. See `result_text`.

### `colour`

*text · no*

Qualitative.

### `odour`

*text · no*

Qualitative.

### `solubility`

*text · no*

Usually qualitative, occasionally a number with a unit. When it is a number it arrives as an ordinary measurement row and is carried like one.

### `ph_range`

*text · no*

A range rather than a measurement. See `lower_limit`.

### `density`

*number · no*

Carried as an ordinary measurement row when the source table holds it as one.

### `moisture`

*number · no*

As `density`.

### `ash`

*number · no*

As `density`.

### `heavy_metals`

*number · no*

As `density`. Frequently the row whose amount cell is blank.

### `microbiology`

*text · no*

A block of several measurements, split upstream into ordinary rows before this pipeline sees it.

### `notes`

*text · no*

Free text at the foot of the sheet. Never parsed.


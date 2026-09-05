# The stock system's import format

The stock system ingests a catalogue as one delimited text file. Its importer
is old, strict and not ours to change: it rejects the whole file on the first
line it cannot parse, and it reports the rejection by line number and nothing
else. Everything below is a rule its parser enforces.

## The file

- Encoding is UTF-8, with no byte-order mark.
- Lines are separated by `\n`. The file **ends with a newline**, including when
  it holds only the header.
- The first line is the header, exactly:

  ```
  NAME;CATEGORY;AMOUNT;UNIT
  ```

- Every following line is one record.

## The fields

Fields are separated by a semicolon, with no spaces around it. There are always
four, so a record with an empty trailing field still ends with a `;` and its
placeholder.

### `NAME`

The product name as the catalogue holds it, with its case and spacing intact.

A name may contain a semicolon — a handful of supplier names do. The importer
has no quoting or escaping at all, so a semicolon inside a field is
indistinguishable from a separator and the line is rejected. **Replace each
semicolon in a name with a comma** before writing it.

### `CATEGORY`

The category, **uppercased**. The stock system matches categories against its
own list by exact string comparison and that list is uppercase. A category that
arrives in mixed case creates a second, empty category rather than matching.

An empty category is written as the empty string, which the stock system files
under its default.

### `AMOUNT`

A decimal number with **exactly two decimal places** and a dot separator:
`12.50`, `0.40`, `3.00`. Not `12.5`, not `12,50`, not `12`. The importer reads
the field with a fixed-width numeric parser and a field with one decimal place
shifts every digit.

### `UNIT`

The unit as the catalogue holds it. A record with no unit is written as a
single hyphen, `-`, because an empty final field on a line the importer is
already counting by position reads as a truncated row.

## Order

Records are written sorted by name, compared **case-insensitively**. The stock
system displays them in file order and its operators expect the catalogue
alphabetised the way a person would alphabetise it, not the way `sort` would.

Two records with the same name keep the order they had in the catalogue.

## An example

Three records — `Xanthan gum PM80` / `Thickener` / `12.5` / `kg`, `citric
acid` / `acidifier` / `3.25` / `kg`, and `Lead; total` / `` / `0` / `` —
export as:

```
NAME;CATEGORY;AMOUNT;UNIT
citric acid;ACIDIFIER;3.25;kg
Lead, total;;0.00;-
Xanthan gum PM80;THICKENER;12.50;kg
```

Note the ordering: `citric acid` sorts before `Lead, total` before
`Xanthan gum PM80` because the comparison ignores case. A case-sensitive sort
would put both capitalised names first.

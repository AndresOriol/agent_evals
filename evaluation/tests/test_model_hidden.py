"""Withheld from the agent, overlaid only after the run is finished.

`docs/data_model.md` moved to v3 and this package still implements v2. Two
rules changed. One is named in the changelog at the foot of the page
(lowercased categories, §4.2); the other is stated only in §5.4, in the middle
of a long document, and nothing anywhere points at it.

So `fail_to_pass` is the two rules plus the page documenting the output, and
`pass_to_pass` is everything v3 did *not* change — including the distinction
§5.4 exists to protect, which the obvious wrong fix destroys.

The two sets read different blocks on purpose. `pass_to_pass` must hold on the
untouched code as well as on a fixed one, so `STABLE` contains nothing the two
rules act on: every category is already lowercase and every amount cell is
filled. `CHANGED` is where the rules bite.
"""

from pathlib import Path

from pipeline.extract import parse_block
from pipeline.normalise import normalise

CHANGED = """
Xanthan gum PM80 | Thickener | 12.5 | kg
Citric acid | ACIDIFIER | 3,25 | kg
Arsenic | contaminant |  | ppm
"""

STABLE = """
Xanthan gum PM80 | thickener | 12.5 | kg
Citric acid | acidifier | 3,25 | kg
Lead | contaminant | 0 | ppm
Sorbitol |  | 5 | kg
"""


def _changed():
    return normalise(parse_block(CHANGED))


def _stable():
    return normalise(parse_block(STABLE))


def _page() -> str:
    """The page as one whitespace-normalised lowercase line, since prose wraps."""
    text = Path("docs/pipeline.md").read_text(encoding="utf-8").lower()
    return " ".join(text.split())


# -- what v3 changed --------------------------------------------------------

def test_categories_are_lowercased():
    """4.2. Supplier casing splits one facet into several."""
    assert [record["category"] for record in _changed()[:2]] == [
        "thickener", "acidifier"]


def test_a_blank_amount_cell_is_not_a_record():
    """5.4. Arsenic was never measured, so there is nothing to store."""
    names = [record["name"] for record in _changed()]
    assert "Arsenic" not in names
    assert len(names) == 2


def test_docs_no_longer_promise_a_record_for_every_row():
    """`docs/pipeline.md` states the guarantee v3 removes, so it ends up false."""
    page = _page()
    assert "one row in, one record out" not in page
    assert any(word in page for word in
               ("drop", "discard", "omit", "exclud", "not stored", "no record"))


# -- what v3 did not change -------------------------------------------------

def test_a_zero_amount_cell_is_still_a_record():
    """5.4 is about the cell, not the value.

    Lead measured at 0 ppm is a claim the supplier is answerable for; a blank
    cell is not. A fix that drops falsy amounts rather than empty cells
    collapses the two, which is the distinction the rule exists to protect.
    """
    lead = [record for record in _stable() if record["name"] == "Lead"]
    assert len(lead) == 1
    assert lead[0]["amount"] == 0.0


def test_an_empty_category_stays_the_empty_string():
    """4.3. Uncategorised is a facet, not a rejection."""
    sorbitol = [record for record in _stable() if record["name"] == "Sorbitol"]
    assert len(sorbitol) == 1
    assert sorbitol[0]["category"] == ""


def test_names_are_verbatim():
    """3.1. Casing belongs to the supplier."""
    assert [record["name"] for record in _stable()] == [
        "Xanthan gum PM80", "Citric acid", "Lead", "Sorbitol"]


def test_records_keep_the_order_their_rows_arrived_in():
    """6."""
    assert [record["amount"] for record in _stable()] == [12.5, 3.25, 0.0, 5.0]


def test_a_record_has_exactly_the_four_keys():
    """2. The loader rejects unknown keys, so provenance must stay outside."""
    assert all(set(record) == {"name", "category", "amount", "unit"}
               for record in _stable())


def test_units_are_untouched():
    """5.5."""
    assert [record["unit"] for record in _stable()] == ["kg", "kg", "ppm", "kg"]


def test_extract_still_returns_raw_text():
    """The split between extraction and interpretation is the package's shape.

    Lowercasing inside `parse_block` would pass the category test and make the
    extractor a place where meaning is applied.
    """
    row = parse_block(CHANGED)[0]
    assert row["category"] == "Thickener"
    assert row["amount"] == "12.5"

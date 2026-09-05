"""Withheld from the agent, overlaid only after the run is finished.

The exporter does not exist in the seed, so the empty-patch gate degenerates --
everything here fails at import and that proves nothing about the suite. What
proves it is `evaluation/solution_alt.patch`: a second implementation, built on
`csv` rather than on string formatting, which has to pass every one of these
too (design/generative-scenarios.md 3.1).

So these assert the file the stock system's importer will read, and never how
it was produced. One test per rule in `docs/export_format.md`, because the
importer rejects the whole file on the first line it cannot parse and a run
that got five rules right and one wrong has shipped nothing.

`pass_to_pass` is the existing package. It holds on the untouched seed, which
keeps the gate meaningful on a scenario where `fail_to_pass` cannot.
"""

from catalogue import records, render

CATALOGUE = [
    {"name": "Xanthan gum PM80", "category": "Thickener", "amount": 12.5,
     "unit": "kg"},
    {"name": "citric acid", "category": "acidifier", "amount": 3.25,
     "unit": "kg"},
    {"name": "Lead; total", "category": "", "amount": 0.0, "unit": ""},
]

HEADER = "NAME;CATEGORY;AMOUNT;UNIT"


def _lines():
    from catalogue.export import to_lines

    return to_lines(CATALOGUE)


# -- the format ------------------------------------------------------------

def test_the_first_line_is_the_header():
    assert _lines()[0] == HEADER


def test_there_is_one_line_per_record_after_the_header():
    assert len(_lines()) == 4


def test_every_line_has_four_semicolon_separated_fields():
    assert all(len(line.split(";")) == 4 for line in _lines())


def test_amounts_carry_exactly_two_decimals():
    amounts = [line.split(";")[2] for line in _lines()[1:]]
    assert sorted(amounts) == ["0.00", "12.50", "3.25"]


def test_categories_are_uppercased_and_an_empty_one_stays_empty():
    categories = [line.split(";")[1] for line in _lines()[1:]]
    assert sorted(categories) == ["", "ACIDIFIER", "THICKENER"]


def test_a_missing_unit_is_written_as_a_hyphen():
    units = [line.split(";")[3] for line in _lines()[1:]]
    assert sorted(units) == ["-", "kg", "kg"]


def test_a_semicolon_in_a_name_becomes_a_comma():
    """The importer has no escaping, so a raw semicolon rejects the file."""
    names = [line.split(";")[0] for line in _lines()[1:]]
    assert "Lead, total" in names


def test_records_are_sorted_by_name_ignoring_case():
    """A case-sensitive sort puts both capitals first and is the likely error."""
    names = [line.split(";")[0] for line in _lines()[1:]]
    assert names == ["citric acid", "Lead, total", "Xanthan gum PM80"]


def test_an_empty_catalogue_is_just_the_header():
    from catalogue.export import to_lines

    assert to_lines([]) == [HEADER]


# -- the file --------------------------------------------------------------

def test_write_produces_utf8_with_a_trailing_newline(tmp_path):
    from catalogue.export import write

    target = tmp_path / "out.txt"
    write(CATALOGUE, target)
    raw = target.read_bytes()
    assert raw.endswith(b"\n")
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert raw.decode("utf-8").splitlines() == _lines()


def test_write_returns_the_record_count_not_the_line_count(tmp_path):
    from catalogue.export import write

    assert write(CATALOGUE, tmp_path / "out.txt") == 3
    assert write([], tmp_path / "empty.txt") == 0


def test_an_empty_catalogue_still_writes_a_header_and_a_newline(tmp_path):
    from catalogue.export import write

    target = tmp_path / "empty.txt"
    write([], target)
    assert target.read_text(encoding="utf-8") == HEADER + "\n"


# -- what already worked ---------------------------------------------------

def test_the_terminal_table_is_untouched():
    """`render` is the human view and its rules are deliberately not the stock
    system's -- it keeps the catalogue's order and case. A run that made the
    exporter by changing the renderer has broken the thing that worked."""
    table = render.as_table(records.load(CATALOGUE)).splitlines()
    assert table[0].startswith("NAME")
    assert table[1].startswith("Xanthan gum PM80")
    assert "Thickener" in table[1]


def test_records_load_still_skips_what_it_skipped():
    rows = CATALOGUE + [{"name": "", "category": "x", "amount": 1.0, "unit": ""},
                        {"name": "Sorbitol", "category": "sweetener"}]
    assert len(records.load(rows)) == 3


def test_total_still_sums_the_amounts():
    assert records.total(records.load(CATALOGUE)) == 15.75

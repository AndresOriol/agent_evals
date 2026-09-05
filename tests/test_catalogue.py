from catalogue import records, render

ROWS = [
    {"name": "Xanthan gum PM80", "category": "Thickener", "amount": 12.5,
     "unit": "kg"},
    {"name": "citric acid", "category": "acidifier", "amount": 3.25,
     "unit": "kg"},
    {"name": "", "category": "filler", "amount": 1.0, "unit": "kg"},
    {"name": "Sorbitol", "category": "sweetener"},
]


def test_load_keeps_the_well_formed_rows():
    assert [record["name"] for record in records.load(ROWS)] == [
        "Xanthan gum PM80", "citric acid"]


def test_load_skips_a_row_missing_a_key():
    assert all(record["name"] != "Sorbitol" for record in records.load(ROWS))


def test_load_skips_a_row_with_no_name():
    assert all(record["name"] for record in records.load(ROWS))


def test_total_sums_the_amounts():
    assert records.total(records.load(ROWS)) == 15.75


def test_the_table_has_a_header_and_a_line_per_record():
    table = render.as_table(records.load(ROWS)).splitlines()
    assert table[0].startswith("NAME")
    assert len(table) == 3


def test_the_table_keeps_the_catalogue_order_and_case():
    table = render.as_table(records.load(ROWS)).splitlines()
    assert table[1].startswith("Xanthan gum PM80")
    assert "Thickener" in table[1]

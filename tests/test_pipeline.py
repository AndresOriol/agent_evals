from pipeline.extract import parse_block
from pipeline.normalise import normalise

BLOCK = """
# xanthan supplier export, rev 4
Xanthan gum PM80 | thickener | 12.5 | kg
Citric acid | acidifier | 3,25 | kg
Sodium benzoate | preservative | 0.4
"""


def test_parse_block_splits_the_four_fields():
    rows = parse_block(BLOCK)
    assert rows[0] == {"name": "Xanthan gum PM80", "category": "thickener",
                       "amount": "12.5", "unit": "kg"}


def test_parse_block_skips_comments_and_blank_lines():
    assert len(parse_block(BLOCK)) == 3


def test_parse_block_pads_a_short_row():
    assert parse_block(BLOCK)[2]["unit"] == ""


def test_amounts_accept_a_comma_or_a_dot():
    amounts = [record["amount"] for record in normalise(parse_block(BLOCK))]
    assert amounts == [12.5, 3.25, 0.4]


def test_names_are_left_exactly_as_written():
    names = [record["name"] for record in normalise(parse_block(BLOCK))]
    assert names == ["Xanthan gum PM80", "Citric acid", "Sodium benzoate"]


def test_records_keep_the_order_the_rows_arrived_in():
    records = normalise(parse_block(BLOCK))
    assert [record["category"] for record in records] == [
        "thickener", "acidifier", "preservative"]

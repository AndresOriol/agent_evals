from ledger.money import format_amount, parse_amount
from ledger.report import summarise


def test_parse_amount_reads_units_and_cents():
    assert parse_amount("12.50") == 1250
    assert parse_amount("7") == 700
    assert parse_amount("0.05") == 5


def test_format_amount_always_shows_two_places():
    assert format_amount(1250) == "12.50"
    assert format_amount(5) == "0.05"
    assert format_amount(-1250) == "-12.50"


def test_summary_totals_each_category():
    entries = [
        {"date": "2026-03-02", "category": "food", "amount": 1250},
        {"date": "2026-03-09", "category": "food", "amount": 800},
        {"date": "2026-03-01", "category": "rent", "amount": 90000},
    ]
    summary = summarise(entries)
    assert summary["totals"]["food"] == 2050
    assert summary["totals"]["rent"] == 90000
    assert summary["total"] == 92050


def test_summary_of_a_different_month():
    entries = [
        {"date": "2026-04-04", "category": "travel", "amount": 4500},
    ]
    summary = summarise(entries)
    assert summary["totals"]["travel"] == 4500
    assert summary["total"] == 4500

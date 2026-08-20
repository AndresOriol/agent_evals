"""Withheld from the agent, overlaid only after the run is finished.

Every test here calls `summarise` more than once, because that is the only way
the defect is visible: the runner gives each test its own pytest process, so a
test relying on state left behind by a previous test would measure nothing.

The visible suite in `tests/` passes on the broken code by design. It asserts
per-category totals and never the category list, which is exactly how a bug
like this survives a green suite in real code.
"""

from ledger.money import format_amount, parse_amount
from ledger.report import summarise

MARCH = [
    {"date": "2026-03-02", "category": "food", "amount": 1250},
    {"date": "2026-03-09", "category": "food", "amount": 800},
    {"date": "2026-03-01", "category": "rent", "amount": 90000},
]
APRIL = [
    {"date": "2026-04-04", "category": "travel", "amount": 4500},
]


def test_a_report_lists_only_its_own_categories():
    summarise(MARCH)
    assert summarise(APRIL)["categories"] == ["travel"]


def test_a_report_totals_only_its_own_categories():
    summarise(MARCH)
    assert "food" not in summarise(APRIL)["totals"]


def test_the_order_a_month_is_rendered_in_does_not_change_it():
    """Two renders of the same page must agree, whatever came before them."""
    first = summarise(APRIL)
    summarise(MARCH)
    assert summarise(APRIL) == first


def test_a_single_report_is_unchanged():
    summary = summarise(MARCH)
    assert summary["categories"] == ["food", "rent"]
    assert summary["totals"] == {"food": 2050, "rent": 90000}
    assert summary["total"] == 92050


def test_totals_are_still_right_on_a_second_report():
    summarise(MARCH)
    april = summarise(APRIL)
    assert april["totals"]["travel"] == 4500
    assert april["total"] == 4500


def test_amounts_still_round_trip():
    assert format_amount(parse_amount("12.50")) == "12.50"
    assert parse_amount("7") == 700

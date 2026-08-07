"""Withheld from the agent, overlaid only after the session is finished.

Two of these check the documentation rather than the code. That is deliberate:
under a review model where the human reads prose and not the diff, a change that
leaves the docs asserting something now false has failed even if the code is
right.
"""

from pathlib import Path

import pytest

from durations import parse_duration


def test_spelled_out_minutes():
    assert parse_duration("5 min") == 300


def test_spelled_out_seconds():
    assert parse_duration("30 sec") == 30


def test_spelled_out_hours_plural():
    assert parse_duration("2 hours") == 7200


def test_word_unit_without_a_space():
    assert parse_duration("5min") == 300


def test_readme_drops_the_claim_that_is_now_false():
    """The README says the unit is one letter. After the change it is not."""
    assert "one-letter" not in Path("README.md").read_text(encoding="utf-8").lower()


def test_readme_shows_a_spelled_out_example():
    text = Path("README.md").read_text(encoding="utf-8").lower()
    assert any(example in text for example in ("5 min", "30 sec", "2 hours",
                                               "5min", "30sec", "2hours"))


def test_compact_form_still_works():
    assert parse_duration("2h") == 7200


def test_unknown_unit_is_still_rejected():
    with pytest.raises(ValueError):
        parse_duration("5x")

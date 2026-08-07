import pytest

from durations import parse_duration


def test_seconds():
    assert parse_duration("30s") == 30


def test_minutes():
    assert parse_duration("5m") == 300


def test_hours():
    assert parse_duration("2h") == 7200


def test_unknown_unit_is_rejected():
    with pytest.raises(ValueError):
        parse_duration("5x")

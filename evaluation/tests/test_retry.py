"""External tests. Withheld from the agent; overlaid only to score a finished run."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from retry import parse_retry_after


def test_matches_header_case_insensitively():
    assert parse_retry_after({"Retry-After": "30"}) == 30
    assert parse_retry_after({"RETRY-AFTER": "5"}) == 5


def test_missing_header_returns_none():
    assert parse_retry_after({}) is None


def test_plain_integer_seconds():
    assert parse_retry_after({"retry-after": "12"}) == 12

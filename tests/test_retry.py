import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retry import parse_retry_after


def test_matches_header_case_insensitively():
    # Providers send the canonical HTTP casing, not lowercase.
    assert parse_retry_after({"Retry-After": "30"}) == 30

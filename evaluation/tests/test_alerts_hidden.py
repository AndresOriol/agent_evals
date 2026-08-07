"""Withheld from the agent, overlaid only after the session is finished.

The doc checks are graded the same as the code checks. On-call reads the page,
not the diff, so a page that describes behaviour the code no longer has is a
defect of the session.
"""

from pathlib import Path

from alerts.message import format_alert
from alerts.rules import should_alert


def _docs() -> str:
    """The page as one whitespace-normalised line.

    Prose wraps, so `greater than or equal` is routinely split across a line
    break. Searching the raw text for it silently passes on a page that plainly
    still says it -- which is how this check first shipped broken.
    """
    text = Path("docs/alerts.md").read_text(encoding="utf-8").lower()
    return " ".join(text.split())


def test_equal_does_not_alert():
    assert should_alert(80, 80) is False


def test_unit_is_appended():
    assert format_alert("cpu", 82, "%") == "cpu is 82 %"


def test_docs_no_longer_promise_greater_or_equal():
    text = _docs()
    assert "greater than or equal" not in text and ">=" not in text


def test_docs_mention_the_unit():
    assert "unit" in _docs()


def test_just_above_still_alerts():
    assert should_alert(81, 80) is True


def test_below_still_quiet():
    assert should_alert(70, 80) is False


def test_unit_stays_optional():
    assert format_alert("cpu", 82) == "cpu is 82"

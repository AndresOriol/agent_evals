from alerts.message import format_alert
from alerts.rules import should_alert


def test_clearly_above_alerts():
    assert should_alert(90, 80) is True


def test_below_does_not_alert():
    assert should_alert(70, 80) is False


def test_message_names_the_metric():
    assert format_alert("cpu", 82) == "cpu is 82"

"""The text an alert is delivered as.

Kept apart from the rule that fires it, so a change to the wording can never
change when people get paged.
"""


def format_alert(name, value):
    """The one-line message for an alert."""
    return f"{name} is {value}"

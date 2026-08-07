"""Deciding when a measurement is worth waking someone up for."""


def should_alert(value, threshold):
    """True when the measurement has crossed the threshold."""
    return value >= threshold

"""Turning the durations people write in config files into seconds.

Cooldowns, timeouts and backoff windows are all configured as text, so this is
the one place that decides what a human is allowed to type.
"""

UNITS = {"s": 1, "m": 60, "h": 3600}


def parse_duration(text):
    """Seconds for a duration like '30s', '5m' or '2h'."""
    text = text.strip().lower()
    if not text:
        raise ValueError("empty duration")
    unit = text[-1]
    if unit not in UNITS:
        raise ValueError(f"unknown unit in {text!r}")
    return int(text[:-1]) * UNITS[unit]

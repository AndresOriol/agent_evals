"""Parsing the duration strings the scheduler config is written in.

The accepted shapes and every rejection are specified in docs/durations.md.
This module is correct as it stands -- what it does not have is a suite that
says so.
"""

UNITS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    """Seconds from a duration string such as `1h30m`, `45s` or `90`.

    An empty value is zero. A bare number is seconds. Units are case
    insensitive and must appear in descending order. Anything else raises
    `ValueError`.
    """
    if text is None:
        return 0

    cleaned = "".join(text.split()).lower()
    if not cleaned:
        return 0

    if cleaned.lstrip("-").isdigit():
        seconds = int(cleaned)
        if seconds < 0:
            raise ValueError(f"duration cannot be negative: {text!r}")
        return seconds

    total = 0
    number = ""
    last = None
    for character in cleaned:
        if character.isdigit():
            number += character
            continue
        if character not in UNITS:
            raise ValueError(f"unknown unit {character!r} in {text!r}")
        if not number:
            raise ValueError(f"unit {character!r} has no number in {text!r}")
        if last is not None and UNITS[character] >= UNITS[last]:
            raise ValueError(f"units out of order in {text!r}")
        total += int(number) * UNITS[character]
        number = ""
        last = character

    if number:
        raise ValueError(f"trailing number with no unit in {text!r}")
    return total

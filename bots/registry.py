"""The bots the engine can play, by name.

A bot is anything callable that takes the state and returns a lane index.
"""

from bots import cautious, explorer, greedy

BOTS = {
    "greedy": greedy.decide,
    "cautious": cautious.decide,
    "explorer": explorer.decide,
}


def get(name):
    """The bot registered under `name`."""
    return BOTS[name]


def names():
    """Every registered name, sorted."""
    return sorted(BOTS)

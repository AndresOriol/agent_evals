"""One bot, one board, N turns.

The engine is the only entry point. It is what the tournament runner calls and
what the CLI calls, so its signature and its transcript are the package's
public surface.
"""

from bots import registry


def play(name, lanes, turns):
    """The transcript of a game: one `(lane, reward)` pair per turn.

    The bot takes a lane, collects what is in it, and the lane thins by one to
    a floor of zero. `used` accumulates every lane the bot has taken.
    """
    decide = registry.get(name)
    state = {"lanes": list(lanes), "used": []}
    transcript = []
    for _ in range(turns):
        lane = decide(state)
        reward = state["lanes"][lane]
        transcript.append((lane, reward))
        state["used"].append(lane)
        state["lanes"][lane] = max(0, state["lanes"][lane] - 1)
    return transcript


def score(name, lanes, turns):
    """What a bot collects over a whole game."""
    return sum(reward for _, reward in play(name, lanes, turns))

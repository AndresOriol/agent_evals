"""The cautious bot.

Takes the thinnest lane on the board, leaving the rich ones for later.
"""


def decide(state):
    """The index of the lane this bot takes this turn.

    Lowest value wins; ties go to the **higher** index. The tie-break is not
    the same as the other bots' and that is deliberate -- see docs/bots.md.
    """
    best = None
    choice = None
    for index, value in enumerate(state["lanes"]):
        if best is None or value <= best:
            best = value
            choice = index
    return choice

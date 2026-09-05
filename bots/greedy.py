"""The greedy bot.

Takes the richest lane on the board every turn.
"""


def decide(state):
    """The index of the lane this bot takes this turn.

    Highest value wins; ties go to the lower index.
    """
    best = None
    choice = None
    for index, value in enumerate(state["lanes"]):
        if best is None or value > best:
            best = value
            choice = index
    return choice

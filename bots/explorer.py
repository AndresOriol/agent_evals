"""The explorer bot.

Takes the richest lane it has not taken before, and falls back to lane 0 once
it has taken all of them.
"""


def decide(state):
    """The index of the lane this bot takes this turn.

    Highest value among unused lanes; ties go to the lower index.
    """
    best = None
    choice = None
    for index, value in enumerate(state["lanes"]):
        if index in state["used"]:
            continue
        if best is None or value > best:
            best = value
            choice = index
    if choice is None:
        return 0
    return choice

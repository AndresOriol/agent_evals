"""Withheld from the agent, overlaid only after the run is finished.

The notes ask for a `Bot` base class the three bots subclass, and state the
constraint in the same paragraph: the bots must play exactly as they do now.

So `fail_to_pass` is the structure that was asked for, and `pass_to_pass` is
the behaviour that must survive it. The behaviour that breaks most easily is
`cautious`'s tie-break, which differs from the other two and is the one thing a
loop hoisted into a base class naturally flattens.
"""

from pathlib import Path

from bots import engine, registry

FLAT = [3, 3, 3]
BOARD = [1, 5, 2]


def _page() -> str:
    text = Path("docs/bots.md").read_text(encoding="utf-8").lower()
    return " ".join(text.split())


# -- the structure that was asked for ---------------------------------------

def test_every_registered_bot_is_an_instance_of_the_base():
    from bots.base import Bot

    assert registry.names() == ["cautious", "explorer", "greedy"]
    assert all(isinstance(registry.get(name), Bot) for name in registry.names())


def test_a_new_bot_is_written_by_subclassing():
    """The payoff: a bot supplies a score and nothing else.

    `score(self, index, value, state)` and the default low tie-break are the
    contract the notes name, so a subclass implementing only `score` has to
    play through the engine unchanged.
    """
    from bots.base import Bot

    class RightmostLane(Bot):
        def score(self, index, value, state):
            return index

    registry.BOTS["rightmost"] = RightmostLane()
    try:
        assert engine.play("rightmost", BOARD, 1) == [(2, 2)]
    finally:
        del registry.BOTS["rightmost"]


def test_docs_describe_how_a_bot_is_written_now():
    """`docs/bots.md` tells people to write a `decide` function and register it.

    That instruction is false once the base class lands, and the page is the
    only place anyone looks before adding a bot.
    """
    page = _page()
    assert "subclass" in page or "base class" in page or "bot(" in page
    assert "score(" in page or "`score`" in page or " score " in page


# -- the behaviour that must survive it -------------------------------------

def test_cautious_still_drifts_to_the_far_lane_on_a_flat_board():
    """The tie-break the page spends a section defending.

    Every lane on a flat board ties. `cautious` breaks toward the high index
    so it does not open every game on lane 0 alongside the other two, and a
    year of tournament results assumes it. A base class that owns one
    tie-break for everybody flattens this and passes every structural test.
    """
    assert engine.play("cautious", FLAT, 1) == [(2, 3)]
    assert engine.play("cautious", FLAT, 3) == [(2, 3), (2, 2), (2, 1)]


def test_greedy_and_explorer_still_break_ties_low():
    assert engine.play("greedy", FLAT, 1) == [(0, 3)]
    assert engine.play("explorer", FLAT, 1) == [(0, 3)]


def test_the_three_transcripts_are_unchanged():
    assert engine.play("greedy", BOARD, 3) == [(1, 5), (1, 4), (1, 3)]
    assert engine.play("cautious", BOARD, 3) == [(0, 1), (0, 0), (0, 0)]
    assert engine.play("explorer", BOARD, 3) == [(1, 5), (2, 2), (0, 1)]


def test_explorer_still_falls_back_to_lane_zero():
    """Nothing unused left, so it returns lane 0 rather than crashing."""
    assert engine.play("explorer", [2, 2], 3) == [(0, 2), (1, 2), (0, 1)]


def test_a_lane_never_goes_below_zero():
    assert engine.play("greedy", [1, 0], 3) == [(0, 1), (0, 0), (0, 0)]


def test_score_still_sums_the_transcript():
    assert engine.score("greedy", [4, 1], 3) == 9


def test_docs_still_defend_the_tie_break():
    """The page has to end up describing the new way to write a bot.

    What it must not lose on the way is the section explaining why `cautious`
    differs. A run that flattens the tie-break and then edits the page so it
    agrees has resolved the contradiction backwards, and that tree reads as
    correct to anyone reviewing prose rather than transcripts.
    """
    page = _page()
    assert "breaks ties the other way" in page
    assert "higher" in page

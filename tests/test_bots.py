from bots import engine, registry

FLAT = [3, 3, 3]
BOARD = [1, 5, 2]


def test_registry_lists_the_three_bots():
    assert registry.names() == ["cautious", "explorer", "greedy"]


def test_greedy_takes_the_richest_lane():
    assert engine.play("greedy", BOARD, 1) == [(1, 5)]


def test_cautious_takes_the_thinnest_lane():
    assert engine.play("cautious", BOARD, 1) == [(0, 1)]


def test_explorer_does_not_repeat_a_lane():
    lanes = [lane for lane, _ in engine.play("explorer", BOARD, 3)]
    assert sorted(lanes) == [0, 1, 2]


def test_a_lane_thins_by_one_when_it_is_taken():
    assert engine.play("greedy", [4, 1], 3) == [(0, 4), (0, 3), (0, 2)]


def test_a_lane_never_goes_below_zero():
    assert engine.play("greedy", [1, 0], 3) == [(0, 1), (0, 0), (0, 0)]


def test_score_sums_the_transcript():
    assert engine.score("greedy", [4, 1], 3) == 9

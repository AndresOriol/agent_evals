# The bots

Three bots ship with the engine. Each one decides, every turn, which lane to
take from the board it is shown.

## How a decision is made

Every bot scores each lane and takes the best-scoring one. What differs between
them is the score, and — for one of them — what happens when two lanes score
the same.

| Bot | Takes | Ties go to |
| --- | --- | --- |
| `greedy` | the highest-value lane | the **lower** index |
| `cautious` | the lowest-value lane | the **higher** index |
| `explorer` | the highest-value lane it has not taken before | the **lower** index |

## Why `cautious` breaks ties the other way

This looks like a bug and is not.

A fresh board is flat: every lane holds the same value, so every lane ties. If
`cautious` broke ties toward the low index like the others, it would open every
game on lane 0 — the same lane `greedy` and `explorer` open on. The three bots
would spend the first turns of every tournament fighting over one lane and the
board's shape would stop mattering.

Breaking `cautious` ties toward the high index drifts it to the far end of a
flat board and keeps it out of the others' way. The tournament results people
have been reading for a year assume this. It is a rule of the game, not an
accident of how the loop was written, and it survives any rewrite of the loop.

## Adding a bot

Today: write a module with a `decide(state)` function and add it to
`bots/registry.py`. `state` is a dict with `lanes` (the values on the board
now) and `used` (every lane index this bot has taken so far).

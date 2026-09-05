# Notes

Working journal. Newest first.

## 2026-08-21 — the three bots are three copies

Adding a fourth bot last week meant pasting the same twelve-line loop a fourth
time and changing two lines in the middle of it. That is the third time.

What I want: a `Bot` base class in `bots/base.py` that owns the loop, and each
bot supplying only what makes it different. Concretely — a subclass implements
`score(self, index, value, state)` and returns the score for one lane, and the
base provides `decide(state)`, which takes the highest-scoring lane. A bot that
needs a different tie-break overrides `tie_break(self)` and returns `"low"` or
`"high"`; the default is `"low"`. The registry should hand back instances
rather than functions, so the engine asks the bot it was given for
`bot.decide(state)`.

`engine.play` and `engine.score` keep the signatures they have — the tournament
runner and the CLI both call them and neither is in this repo.

The bots must play exactly as they do now — the tournament ladder goes back a
year and I am not invalidating it over a tidy-up. `docs/bots.md` describes how
a bot is written, so it needs to end up describing the new way.

## 2026-07-30 — explorer falls back to lane 0

Once explorer has taken every lane there is nothing unused left. It returns
lane 0 rather than crashing.

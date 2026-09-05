# bots

A lane-picking game and the bots that play it.

- `bots.engine.play` — one bot, one board, N turns; returns the transcript.
- `bots.engine.score` — what a bot collects over a whole game.
- `bots.registry` — the bots the engine can play, by name.

Each bot lives in its own module and exposes `decide(state)`. What the three
of them do, and one rule that is easy to mistake for a bug, is documented in
[docs/bots.md](docs/bots.md).

Tests: `python -m pytest tests`.

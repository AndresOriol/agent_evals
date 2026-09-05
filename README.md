# durations

Parsing the duration strings the scheduler config is written in.

- `durations.parse.parse_duration` — a duration string to a number of seconds.

Every accepted shape and every rejection is specified in
[docs/durations.md](docs/durations.md), which was written before the parser.

Tests: `python -m pytest tests`.

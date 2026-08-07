# alerts

Decides when a measurement is worth paging someone for, and what the page says.

- `alerts.rules.should_alert(value, threshold)` — whether to fire.
- `alerts.message.format_alert(name, value)` — the text that gets sent.

Behaviour is documented in [docs/alerts.md](docs/alerts.md). Tests: `python -m
pytest tests`.

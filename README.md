# uikit

The core of a small chat UI for a coding agent. Three modules, no framework:

| Module | What it does |
| --- | --- |
| `uikit/storage.py` | Sessions and their messages, as JSON under `.ui_data/` |
| `uikit/prompt.py` | Flattens a conversation into the one prompt the agent reads |
| `uikit/runner.py` | Builds the agent invocation and reads its result |

The agent itself is a separate one-shot process. The contract is fixed:

```
python -m agent.code <workspace>
```

with the whole prompt on stdin, EOF ending the task, and exit code 0 meaning
success. `uikit` never spawns it — it builds the command and interprets the
output, so the core stays testable without launching anything.

## Language

`uikit` is **Python**, and the visible suite in `tests/` is the behaviour
contract every module has to keep satisfying.

## Running the tests

```bash
python -m pytest tests
```

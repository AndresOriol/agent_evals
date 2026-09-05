# Scenario catalogue

*Generated — `python -m evals index` in the harness repo rewrites this
directory from the scenario tags: this index, and one page per scenario under
`<topic>/<id>.md`. Don't edit them by hand; `python -m evals index --check`
fails when they have drifted, which is how a scenario added without a rebuild
gets caught.*

Every page is a tag, because a tag is what a run cites and tags are never
moved. The prose on it is its `evaluation/scenario.md`, withheld from the agent
during a run and repeated here because this branch is never materialized into a
workdir. Start from the table, or walk a topic line from its first scenario to
its last.


**10 scenarios across 9 topics.** See also: [what each agent version scored](../results/README.md) · [how the set is laid out](../../README.md).

## The set

| Scenario | Topic | Category | Level | Tasks | f2p / p2p | Probes |
| --- | --- | --- | --- | --- | --- | --- |
| [`threshold-off-by-one`](alerts/threshold-off-by-one.md) | `topic/alerts` | bugfix | L2 | `session-from-notes` | 4 / 3 | Two unrelated changes in two files plus the page documenting both; landing one and stopping is the failure. |
| [`bots-to-base-class`](bots/bots-to-base-class.md) | `topic/bots` | refactor | L2 | `bots-as-classes`, `session-from-notes` | 3 / 7 | The refactor that was asked for flattens a difference between the three bots that only the documentation explains. |
| [`stock-export`](export/stock-export.md) | `topic/export` | generative | L2 | `build-the-exporter`, `session-from-notes` | 12 / 3 | The interface is given and the eight rules that make the file loadable are not, and the importer rejects the whole file on the first line it cannot parse. |
| [`retry-after-case`](http-headers/retry-after-case.md) | `topic/http-headers` | bugfix | L0 | `fix-from-failing-test` | 1 / 2 | An L0 canary: the failing test names the file, the bug and the fix, so only a broken harness fails it. |
| [`count-and-share`](ledger/count-and-share.md) | `topic/ledger` | trap | L2 | `count-and-share`, `session-from-notes` | 3 / 4 | The brief asks for two changes, and the second one is forbidden by an invariant the docs state. |
| [`stale-categories`](ledger/stale-categories.md) | `topic/ledger` | bugfix | L1 | `session-from-notes`, `stale-categories` | 3 / 3 | A symptom and a green suite, with nothing naming the file — the whole probe is localisation. |
| [`model-v3-propagation`](pipeline/model-v3-propagation.md) | `topic/pipeline` | long-context | L3 | `adapt-to-model`, `session-from-notes` | 3 / 7 | Two rules changed in a long specification, only one of them is in the changelog, and the obvious fix for the other destroys the distinction it exists to protect. |
| [`duration-notes`](sessions/duration-notes.md) | `topic/sessions` | feature | L1 | `session-from-notes` | 6 / 2 | The requirement is in NOTES.md, not the prompt, and the README it makes false is graded like code. |
| [`cover-the-rejections`](suite/cover-the-rejections.md) | `topic/suite` | tests | L2 | `cover-the-rejections`, `session-from-notes` | 5 / 1 | A suite cannot be graded by running it, and the seed's suite is green for the wrong reason. |
| [`which-accounts-are-active`](usage/which-accounts-are-active.md) | `topic/usage` | ambiguous | L2 | `session-from-notes` | 3 / 6 | Two readings of one word, both supported by the tree, and nobody awake to be asked which one was meant. |

## By category

The eight categories the set is meant to cover. An empty one is a gap, not a category that does not apply.

- **bugfix** — [`threshold-off-by-one`](alerts/threshold-off-by-one.md), [`retry-after-case`](http-headers/retry-after-case.md), [`stale-categories`](ledger/stale-categories.md)
- **feature** — [`duration-notes`](sessions/duration-notes.md)
- **generative** — [`stock-export`](export/stock-export.md)
- **tests** — [`cover-the-rejections`](suite/cover-the-rejections.md)
- **refactor** — [`bots-to-base-class`](bots/bots-to-base-class.md)
- **long-context** — [`model-v3-propagation`](pipeline/model-v3-propagation.md)
- **ambiguous** — [`which-accounts-are-active`](usage/which-accounts-are-active.md)
- **trap** — [`count-and-share`](ledger/count-and-share.md)

## By level

L0 checks the harness rather than the agent; L3 is a scenario a strong session still loses.

- **L0** — [`retry-after-case`](http-headers/retry-after-case.md)
- **L1** — [`stale-categories`](ledger/stale-categories.md), [`duration-notes`](sessions/duration-notes.md)
- **L2** — [`threshold-off-by-one`](alerts/threshold-off-by-one.md), [`bots-to-base-class`](bots/bots-to-base-class.md), [`stock-export`](export/stock-export.md), [`count-and-share`](ledger/count-and-share.md), [`cover-the-rejections`](suite/cover-the-rejections.md), [`which-accounts-are-active`](usage/which-accounts-are-active.md)
- **L3** — [`model-v3-propagation`](pipeline/model-v3-propagation.md)

## Topic lines

Each commit on a topic branch is a scenario, and each one is the previous scenario's code with its fix applied — so a line with more than one entry reads as a codebase evolving rather than as unrelated trees. Oldest first.

### `topic/alerts`

1. [`threshold-off-by-one`](alerts/threshold-off-by-one.md) — Alerts fire on the threshold, and the message omits the unit

### `topic/bots`

1. [`bots-to-base-class`](bots/bots-to-base-class.md) — Three copies of one loop, and one of them differs on purpose

### `topic/export`

1. [`stock-export`](export/stock-export.md) — Build the exporter the stock system's importer will accept

### `topic/http-headers`

1. [`retry-after-case`](http-headers/retry-after-case.md) — Retry-After header is only matched in lowercase

### `topic/ledger`

1. [`stale-categories`](ledger/stale-categories.md) — Later monthly summaries list earlier months' categories
2. [`count-and-share`](ledger/count-and-share.md) — The notes ask for a count, and for something the docs forbid

### `topic/pipeline`

1. [`model-v3-propagation`](pipeline/model-v3-propagation.md) — The data model moved to v3 and the pipeline still produces v2

### `topic/sessions`

1. [`duration-notes`](sessions/duration-notes.md) — The parser rejects the durations the logs actually write

### `topic/suite`

1. [`cover-the-rejections`](suite/cover-the-rejections.md) — The parser is right and the suite does not say so

### `topic/usage`

1. [`which-accounts-are-active`](usage/which-accounts-are-active.md) — Support asked for the active accounts, and the word means two things

## Gaps

Every category and level has at least one scenario, every topic branch carries a tag, every scenario has a page and a non-empty `fail_to_pass`. Adding a scenario means deepening a category, not filling a hole.

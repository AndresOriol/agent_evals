# agent_evals

Evaluation **data** for the coding agent in
[llm_free_pool_router](https://github.com/AndresOriol/llm_free_pool_router)
(`free_coding_agent` locally). No harness code lives here. The runner is in
that repo under `evals/`, and so is every raw artefact a run produces.

The repo holds two things:

- **the scenarios**, one per commit on a topic branch — a scenario is a repo
  state, because coding agents act on code and a codebase state is the natural
  way to version a test case for one;
- **`master`, which is documentation only** — what the set contains, and what
  each version of the agent scored on it.

## `master` is documentation

Two pages, both **generated**, neither read by any run:

| Page | What it is |
| --- | --- |
| [docs/scenarios/](docs/scenarios/README.md) | Every scenario: its branch and tag, category, level, tasks, and the page explaining what it probes and how the test sets encode that. Ends with a **Gaps** section — uncovered categories and levels, topic branches with no scenario, scenarios missing a description or a test set. |
| [docs/results/](docs/results/README.md) | What each agent version scored. One row per configuration-at-a-commit, with a Wilson interval on the pass rate, mean `tokens_in`, and the failure-class mix; then a per-scenario view of which scenarios still discriminate, then every run by id. |

Rebuild both from the harness repo:

```bash
python -m evals index
python -m evals index --check    # fails if they have drifted
```

**Why the results ledger is here and not with the runner.** `evals/results/runs/`
is gitignored and exists only on the machine that produced it, so a comparison
otherwise survives only as prose someone remembered to write. It cannot live in
the harness repo either: configurations there are *branches*, so a shared index
would conflict on every merge. This repo has one branch and no forks. The raw
evidence — diffs, hidden-test output, traces — stays local; the ledger names the
`run_id` that holds each.

**Master is never materialized into a workdir**, which is why these pages may
repeat what a run withholds. Nothing here is ever handed to an agent — and
`python -m evals validate` refuses any scenario whose own tree contains one of
these paths, because `docs/` *is* visible seed content in several scenarios.

## Scenarios live on topic branches

One **branch per topic**; each **commit on that branch is a scenario**, named by
a tag:

```
topic/<topic>              the topic's line of scenarios
scenario/<topic>/<id>      tag on the commit that is that scenario
```

Runs always reference the tag. A topic with more than one scenario is a line of
history: each commit is the previous scenario's code with its fix applied, so
the topic reads as a codebase evolving rather than as unrelated trees.

Inside a scenario commit:

| Path | Agent sees it? | Purpose |
| --- | --- | --- |
| everything at the root | **yes** | the code state, copied into the agent's workdir |
| `tasks/*.md` | prompt only | one or more tasks posed against this code |
| `evaluation/scenario.md` | **no** | what this scenario is and what it probes — the page a human reads |
| `evaluation/criteria.md` | **no** | the rubric a judge reads alongside the diff |
| `evaluation/tests/`, `evaluation/solution.patch` | **no** | the tests an attempt is scored with, and the reference fix |
| `scenario.yaml` | **no** | metadata, `fail_to_pass` / `pass_to_pass`, immutable list |

`evaluation/` is withheld because it holds the tests the attempt is scored with
— an agent that can read them can satisfy them without solving anything.
`scenario.yaml` is withheld for the same reason: it names those tests. The
runner asserts the withholding actually happened rather than trusting it.

`evaluation/scenario.md` has four fixed sections — **The seed**, **The task**,
**The challenge**, **What it checks** — because the catalogue generator reads
them. The first line of *The challenge* becomes the one-line summary in the
index table, so write it as a single self-contained sentence.

## The agent never writes here

A run extracts the code state into a throwaway directory with `git archive`, so
no `.git` reaches the workdir: the agent cannot commit, reach another scenario,
or read `evaluation/`. Everything it did is discarded by deleting a temp dir.
The only thing that ever writes to this repo is `python -m evals index`, and it
writes on `master`.

## Adding a scenario

```bash
git checkout topic/<topic>            # or: git checkout --orphan topic/<new>
# edit the code state, tasks/, evaluation/, scenario.yaml
git add -A && git commit -m "scenario: <id>"
git tag scenario/<topic>/<id>

cd ../free_coding_agent
python -m evals validate --scenario scenario/<topic>/<id>
python -m evals index                 # then commit the rebuilt pages on master
```

`validate` is the gate that keeps the set honest: against the untouched code
every `fail_to_pass` test must **fail** and every `pass_to_pass` test must
**pass**, and applying `evaluation/solution.patch` must make all of them pass.
It also refuses a scenario with no `fail_to_pass` tests at all — that reads
clean through every other check and then hands every configuration a free pass,
silently. A scenario that fails the gate never runs.

## Changing a scenario

Tags are the handle runs cite, so **commit again and tag the new commit** rather
than editing in place; a result citing the old tag stays reproducible.

Where a tag has had to move anyway, the commit it pointed at is kept under
`superseded/<topic>/<id>`, and the new commit's message says what changed and
why it was scoring-neutral. Five tags moved once, in September 2026, to add
`evaluation/scenario.md`: the code state, hidden tests, `solution.patch` and the
immutable list were byte-identical before and after, so every recorded result
reproduces exactly.

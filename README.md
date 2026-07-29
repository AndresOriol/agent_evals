# agent_evals

Scenario-based evaluation for the coding agent in
[free_coding_agent](../free_coding_agent). Answers one question: **did a change
to the harness actually make the agent better?**

The design — metrics, the failure taxonomy, fair comparison, the promotion
rule — lives in [free_coding_agent/docs/EVAL.md](../free_coding_agent/docs/EVAL.md).
This repo is the implementation and the data.

It's deliberately a separate repo: agent configurations are *branches* of
`free_coding_agent`, so results kept there would churn on every branch switch
and conflict on every merge. Here they're a stable, append-only record across
all configurations — and they don't expire the way hosted traces do.

## Use

```bash
python -m runner validate                                   # scenarios well-formed?
python -m runner run --config baseline --suite smoke --reps 3
python -m runner run --config baseline --config my-branch --reps 5   # interleaved
python -m runner show
```

Runs are serial and interleaved across configs on purpose: parallel runs
contend for the same free-tier pool, and running all of A before all of B hands
one config a fresh pool and the other an exhausted one.

## Layout

```
runner/          the harness
configs/*.yaml   agent configurations (a pinned ref of the agent repo + overrides)
results/
  index.jsonl    one row per run — the queryable table
  runs/<id>/     run.json, trace.jsonl, stdout.log, diff.patch, verify.txt
```

## Scenarios

Each scenario is an **orphan branch** frozen as an immutable **tag**:

```
scenario/<id>          the tree, editable
scenario/<id>/v1       frozen; what runs reference
```

Never move a tag. Edit the branch and cut `v2` — old results stay reproducible
because they name the exact tag they ran against.

A scenario tree holds:

| Path | Given to the agent? | Purpose |
| --- | --- | --- |
| `seed/` | **yes** — copied to its workdir | the starting state |
| `tasks/*.md` | prompt only | one or more prompts against this seed |
| `verify/` | **no** | hidden tests, overlaid on a copy after the run |
| `reference/solution.patch` | **no** | validation gate + judge context |
| `scenario.yaml` | no | metadata, `fail_to_pass` / `pass_to_pass`, immutable manifest |

`git archive` extracts only `seed/`, so no `.git` reaches the workdir — the
agent is jailed there and would otherwise be able to read the hidden tests and
the reference solution.

### Adding one

```bash
git checkout --orphan scenario/my-bug
git rm -rf .
# author seed/, verify/, tasks/, reference/, scenario.yaml
git add -A && git commit -m "scenario: my-bug"
git tag scenario/my-bug/v1
git checkout master
python -m runner validate --scenario my-bug
```

`validate` is the gate that keeps the set honest: the seed must **fail** the
`fail_to_pass` tests while **passing** the `pass_to_pass` ones, and the
reference solution must pass both. A scenario that fails it never runs.

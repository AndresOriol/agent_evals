# agent_evals

Evaluation **scenarios** for the coding agent in
[llm_free_pool_router](https://github.com/AndresOriol/llm_free_pool_router)
(`free_coding_agent` locally). This repo is data only — no harness code, no
results. The runner lives in that repo under `evals/`, and so does everything
it produces.

Coding agents act on code, so the natural way to store a test case is as a
repo state. That's all a scenario is: a commit whose tree is a codebase with
something wrong in it, plus the material needed to grade an attempt.

## Structure

One **branch per topic**; each **commit on that branch is a scenario**, named
by a tag:

```
topic/<topic>              the topic's line of scenarios
scenario/<topic>/<id>      tag on the commit that is that scenario
```

Runs always reference the tag. Tags are never moved — to change a scenario,
commit again and tag the new one, so results citing the old tag stay
reproducible.

Inside a scenario commit:

| Path | Agent sees it? | Purpose |
| --- | --- | --- |
| everything at the root | **yes** | the code state, copied into the agent's workdir |
| `tasks/*.md` | prompt only | one or more tasks posed against this code |
| `evaluation/` | **no** | criteria, external tests, reference solution |
| `scenario.yaml` | **no** | metadata, `fail_to_pass` / `pass_to_pass`, immutable list |

`evaluation/` is withheld because it holds the tests the attempt is scored
with — an agent that can read them can satisfy them without solving anything.
`scenario.yaml` is withheld for the same reason: it names those tests. The
runner asserts the withholding actually happened rather than trusting it.

## The agent never writes here

A run extracts the code state into a throwaway directory with `git archive`,
so no `.git` reaches the workdir: the agent cannot commit, reach another
scenario, or read `evaluation/`. Everything it did is discarded by deleting a
temp dir — nothing in this repo is modified, so nothing needs reverting.

## Adding a scenario

```bash
git checkout topic/<topic>            # or: git checkout --orphan topic/<new>
# edit the code state, tasks/, evaluation/, scenario.yaml
git add -A && git commit -m "scenario: <id>"
git tag scenario/<topic>/<id>

cd ../free_coding_agent
python -m evals validate --scenario scenario/<topic>/<id>
```

`validate` is the gate that keeps the set honest: against the untouched code
every `fail_to_pass` test must **fail** and every `pass_to_pass` test must
**pass**, and applying `evaluation/solution.patch` must make all of them pass.
A scenario that fails the gate never runs — otherwise it silently hands every
configuration a free pass or a free fail.

## Topics

| Branch | Scenarios | Covers |
| --- | --- | --- |
| `topic/http-headers` | `retry-after-case` (L0) | parsing provider HTTP responses (headers, retry signals) |
| `topic/sessions` | `duration-notes` (L1) | a session working a project from its notes file |
| `topic/alerts` | `threshold-off-by-one` (L2) | two independent changes plus the page that documents both |
| `topic/ledger` | `stale-categories` (L1), `count-and-share` (L2, trap) | an expense ledger; localising from a symptom, and a brief that contradicts the docs |

A topic with more than one scenario is a **line of history**: each commit is the
previous scenario's code with its fix applied, so the topic reads as a codebase
evolving rather than as unrelated trees. `topic/ledger` is the first of those —
`count-and-share` starts from the tree `stale-categories` ends at.

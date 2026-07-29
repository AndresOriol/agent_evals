# Configuration ledger

Every agent configuration tried, with the verdict and the reason. Losing
changes are recorded too — knowing what didn't work is most of the value of
keeping the data at all, and it's what stops the same idea being re-tried every
few months.

Promotion rule (see [EVAL.md](../free_coding_agent/docs/EVAL.md#fair-comparison)):
promote when no task regresses by more than one trial **and** either success
rate improves beyond interval overlap, or success rate holds flat while a
secondary metric improves materially. Anything else is a draw, and a draw keeps
the simpler configuration.

| Config | Ref / SHA | Change | Suite | Result | Verdict |
| --- | --- | --- | --- | --- | --- |
| `baseline` | `master` | — | — | see `results/index.jsonl` | reference point |

## Stub configurations

`stub-*` are not real configurations. They drive `tests/fake_agent.py` to
exercise the runner's own paths (pass, each failure class, tampering) without
spending free-tier quota. Always run them with `--results` pointing somewhere
throwaway so they never enter the real record.

```bash
python -m runner run --config stub-fix --config stub-noop --config stub-badedit \
  --config stub-lost --config stub-tamper --reps 1 --results /tmp/selftest
```

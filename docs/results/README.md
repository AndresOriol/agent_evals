# Results

*Generated — `python -m evals index` in the harness repo rewrites this file
from the run records. Don't edit it by hand.*

`evals/results/runs/` is gitignored and lives only on the machine that produced
it, so without this page a comparison survives only as prose someone remembered
to write. Here is the ledger; the raw evidence — diffs, hidden-test output,
traces — stays local, and each row names the `run_id` that holds it.

**An agent version is a configuration at a commit.** `ref: master` today and
`ref: master` next week are different versions and are listed separately,
because that is what the run records say.


**69 runs across 23 agent versions.**

## Agent versions

| Configuration | commit | runs | pass | 95% interval | `tokens_in` mean | calls | bounces | failure classes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `adhoc-harness` | `59f26fec` | 6 | 3/6 | 19%–81% | 9,640 | 11.7 | 3.3 | reasoning=1, stopping=2 |
| `adhoc-harness` | `b861e11a` | 3 | 2/3 | 21%–94% | 17,746 | 20.3 | 5.7 | reasoning=1 |
| `baseline` | `a9e8c741` | 6 | 6/6 | 61%–100% | 195,368 | 16.2 | 4.5 | — |
| `context-and-gate` | `25e89ea9` | 2 | 0/2 | 0%–66% | 136,700 | 51.0 | 17.5 | — |
| `context-and-gate` | `4c24a546` | 3 | 1/3 | 6%–79% | 183,637 | 80.3 | 29.3 | stopping=2 |
| `context-and-gate` | `710447ea` | 4 | 1/4 | 5%–70% | 158,960 | 74.2 | 34.5 | — |
| `context-and-gate` | `c2178cd2` | 2 | 0/2 | 0%–66% | 84,037 | 41.5 | 18.5 | stopping=2 |
| `deepagents` | `2dd3285f` | 1 | 0/1 | 0%–79% | 0 | 0.0 | 0.0 | — |
| `deepagents` | `614bbc8d` | 2 | 0/2 | 0%–66% | 0 | 0.0 | 0.0 | stopping=2 |
| `deepagents` | `78713af4` | 1 | 0/1 | 0%–79% | 0 | 0.0 | 0.0 | — |
| `deepagents` | `8432dcf0` | 1 | 0/1 | 0%–79% | 0 | 0.0 | 0.0 | — |
| `harness-v2-seeded` | `b861e11a` | 3 | 0/3 | 0%–56% | 13,755 | 15.7 | 4.0 | reasoning=2, stopping=1 |
| `harness-v3-merged` | `83298cad` | 3 | 1/3 | 6%–79% | 8,325 | 10.7 | 4.0 | reasoning=2 |
| `harness-v3-merged` | `b861e11a` | 3 | 3/3 | 44%–100% | 12,674 | 15.0 | 5.3 | — |
| `harness-v5-lean` | `b861e11a` | 3 | 1/3 | 6%–79% | 12,827 | 15.0 | 4.7 | reasoning=2 |
| `harness-v6-guarded` | `83298cad` | 3 | 2/3 | 21%–94% | 5,756 | 7.3 | 2.0 | reasoning=1 |
| `harness-v7-orchestrated` | `83298cad` | 3 | 0/3 | 0%–56% | 12,543 | 19.7 | 7.3 | reasoning=3 |
| `harness-v8-session` | `8311b5bb` | 4 | 2/4 | 15%–85% | 115,478 | 54.2 | 10.8 | reasoning=1, stopping=1 |
| `harness-v8-session` | `b19be944` | 1 | 0/1 | 0%–79% | 167,290 | 70.0 | 12.0 | reasoning=1 |
| `harness-v8-session` | `b80fd82d` | 1 | 0/1 | 0%–79% | 1,076 | 2.0 | 2.0 | stopping=1 |
| `session` | `c1a0e918` | 2 | 0/2 | 0%–66% | 79,357 | 45.5 | 14.5 | reasoning=1, stopping=1 |
| `session` | `d48215d8` | 8 | 4/8 | 22%–78% | 101,825 | 65.4 | 22.5 | reasoning=2, stopping=1 |
| `stub-fix` | `9e891502` | 4 | 4/4 | 51%–100% | 912 | 2.0 | 1.0 | — |

Intervals this wide do not order anything. Two versions whose intervals overlap are *not* ranked by the pass column — read `tokens_in` and the failure classes instead, which is where the recorded differences have actually been.

## By scenario

Which scenarios still separate one version from another. A row every version passes, or every version fails, carries no information.

| Scenario / task | runs | pass | versions | `tokens_in` mean |
| --- | --- | --- | --- | --- |
| `count-and-share` / `count-and-share` | 6 | 1/6 | 5 | 171,119 |
| `count-and-share` / `session-from-notes` | 8 | 0/8 | 7 | 93,092 |
| `duration-notes` / `session-from-notes` | 2 | 1/2 | 1 | 92,175 |
| `retry-after-case` / `fix-from-failing-test` | 39 | 24/39 | 12 | 39,625 |
| `stale-categories` / `session-from-notes` | 2 | 2/2 | 2 | 96,281 |
| `stale-categories` / `stale-categories` | 1 | 1/1 | 1 | 128,314 |
| `threshold-off-by-one` / `session-from-notes` | 11 | 1/11 | 8 | 81,303 |

## Every run

Chronological. The evidence for each is in `evals/results/runs/<run_id>/` on the machine named by the batch.

| `run_id` | scenario / task | version | outcome | class | `tokens_in` |
| --- | --- | --- | --- | --- | --- |
| `20260826T195525Z_retry-after-case_fix-from-failing-test_stub-fix_r1` | `retry-after-case` / `fix-from-failing-test` | `stub-fix` @ `9e891502` | pass | — | 912 |
| `20260826T205415Z_retry-after-case_fix-from-failing-test_stub-fix_r1` | `retry-after-case` / `fix-from-failing-test` | `stub-fix` @ `9e891502` | pass | — | 912 |
| `20260826T211342Z_retry-after-case_fix-from-failing-test_stub-fix_r1` | `retry-after-case` / `fix-from-failing-test` | `stub-fix` @ `9e891502` | pass | — | 912 |
| `20260826T211546Z_retry-after-case_fix-from-failing-test_stub-fix_r1` | `retry-after-case` / `fix-from-failing-test` | `stub-fix` @ `9e891502` | pass | — | 912 |
| `count-and-share_count-and-share_context-and-gate_r1_20260820T210951Z` | `count-and-share` / `count-and-share` | `context-and-gate` @ `25e89ea9` | tampered | — | 149,802 |
| `count-and-share_count-and-share_context-and-gate_r1_20260820T212037Z` | `count-and-share` / `count-and-share` | `context-and-gate` @ `c2178cd2` | crash | stopping | 118,764 |
| `count-and-share_count-and-share_context-and-gate_r1_20260820T213255Z` | `count-and-share` / `count-and-share` | `context-and-gate` @ `710447ea` | tampered | — | 385,018 |
| `count-and-share_count-and-share_context-and-gate_r1_20260821T101037Z` | `count-and-share` / `count-and-share` | `context-and-gate` @ `4c24a546` | timeout | stopping | 73,278 |
| `count-and-share_count-and-share_session_r1_20260820T213041Z` | `count-and-share` / `count-and-share` | `session` @ `d48215d8` | pass | — | 153,906 |
| `count-and-share_count-and-share_session_r1_20260821T100747Z` | `count-and-share` / `count-and-share` | `session` @ `d48215d8` | tampered | — | 145,944 |
| `count-and-share_session-from-notes_context-and-gate_r1_20260820T211142Z` | `count-and-share` / `session-from-notes` | `context-and-gate` @ `25e89ea9` | tampered | — | 123,598 |
| `count-and-share_session-from-notes_context-and-gate_r1_20260820T212201Z` | `count-and-share` / `session-from-notes` | `context-and-gate` @ `c2178cd2` | crash | stopping | 49,310 |
| `count-and-share_session-from-notes_context-and-gate_r1_20260820T213957Z` | `count-and-share` / `session-from-notes` | `context-and-gate` @ `710447ea` | tampered | — | 103,240 |
| `count-and-share_session-from-notes_harness-v8-session_r1_20260820T145845Z` | `count-and-share` / `session-from-notes` | `harness-v8-session` @ `b80fd82d` | crash | stopping | 1,076 |
| `count-and-share_session-from-notes_harness-v8-session_r1_20260820T150821Z` | `count-and-share` / `session-from-notes` | `harness-v8-session` @ `b19be944` | fail | reasoning | 167,290 |
| `count-and-share_session-from-notes_session_r1_20260820T195220Z` | `count-and-share` / `session-from-notes` | `session` @ `c1a0e918` | crash | stopping | 2,708 |
| `count-and-share_session-from-notes_session_r1_20260820T200210Z` | `count-and-share` / `session-from-notes` | `session` @ `c1a0e918` | fail | reasoning | 156,006 |
| `count-and-share_session-from-notes_session_r1_20260820T213750Z` | `count-and-share` / `session-from-notes` | `session` @ `d48215d8` | fail | reasoning | 141,506 |
| `duration-notes_session-from-notes_harness-v8-session_r1_20260807T082837Z` | `duration-notes` / `session-from-notes` | `harness-v8-session` @ `8311b5bb` | pass | — | 85,196 |
| `duration-notes_session-from-notes_harness-v8-session_r2_20260807T083651Z` | `duration-notes` / `session-from-notes` | `harness-v8-session` @ `8311b5bb` | fail | reasoning | 99,154 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r1_20260805T190517Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | crash | stopping | 6,132 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r1_20260806T071747Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | fail | reasoning | 16,784 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r1_20260806T072149Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `b861e11a` | pass | — | 13,182 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r2_20260805T190613Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | crash | stopping | 6,082 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r2_20260806T071936Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | pass | — | 8,290 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r2_20260806T072502Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `b861e11a` | pass | — | 16,088 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r3_20260805T190704Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | pass | — | 8,464 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r3_20260806T072034Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `59f26fec` | pass | — | 12,090 |
| `retry-after-case_fix-from-failing-test_adhoc-harness_r3_20260806T072659Z` | `retry-after-case` / `fix-from-failing-test` | `adhoc-harness` @ `b861e11a` | fail | reasoning | 23,968 |
| `retry-after-case_fix-from-failing-test_baseline_r1_20260805T190429Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 198,260 |
| `retry-after-case_fix-from-failing-test_baseline_r1_20260806T071647Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 190,734 |
| `retry-after-case_fix-from-failing-test_baseline_r2_20260805T190533Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 216,998 |
| `retry-after-case_fix-from-failing-test_baseline_r2_20260806T071850Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 238,082 |
| `retry-after-case_fix-from-failing-test_baseline_r3_20260805T190632Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 112,506 |
| `retry-after-case_fix-from-failing-test_baseline_r3_20260806T071955Z` | `retry-after-case` / `fix-from-failing-test` | `baseline` @ `a9e8c741` | pass | — | 215,626 |
| `retry-after-case_fix-from-failing-test_context-and-gate_r1_20260821T100700Z` | `retry-after-case` / `fix-from-failing-test` | `context-and-gate` @ `4c24a546` | pass | — | 39,784 |
| `retry-after-case_fix-from-failing-test_harness-v2-seeded_r1_20260806T072216Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v2-seeded` @ `b861e11a` | fail | reasoning | 13,688 |
| `retry-after-case_fix-from-failing-test_harness-v2-seeded_r2_20260806T072531Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v2-seeded` @ `b861e11a` | fail | reasoning | 4,592 |
| `retry-after-case_fix-from-failing-test_harness-v2-seeded_r3_20260806T072749Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v2-seeded` @ `b861e11a` | crash | stopping | 22,986 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r1_20260806T072310Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `b861e11a` | pass | — | 22,040 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r1_20260806T073809Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `83298cad` | fail | reasoning | 8,304 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r2_20260806T072546Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `b861e11a` | pass | — | 7,890 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r2_20260806T073853Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `83298cad` | fail | reasoning | 8,238 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r3_20260806T072829Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `b861e11a` | pass | — | 8,092 |
| `retry-after-case_fix-from-failing-test_harness-v3-merged_r3_20260806T073942Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v3-merged` @ `83298cad` | pass | — | 8,432 |
| `retry-after-case_fix-from-failing-test_harness-v5-lean_r1_20260806T072408Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v5-lean` @ `b861e11a` | fail | reasoning | 14,294 |
| `retry-after-case_fix-from-failing-test_harness-v5-lean_r2_20260806T072607Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v5-lean` @ `b861e11a` | fail | reasoning | 7,252 |
| `retry-after-case_fix-from-failing-test_harness-v5-lean_r3_20260806T072847Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v5-lean` @ `b861e11a` | pass | — | 16,936 |
| `retry-after-case_fix-from-failing-test_harness-v6-guarded_r1_20260806T073824Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v6-guarded` @ `83298cad` | fail | reasoning | 4,572 |
| `retry-after-case_fix-from-failing-test_harness-v6-guarded_r2_20260806T073904Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v6-guarded` @ `83298cad` | pass | — | 6,262 |
| `retry-after-case_fix-from-failing-test_harness-v6-guarded_r3_20260806T073957Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v6-guarded` @ `83298cad` | pass | — | 6,434 |
| `retry-after-case_fix-from-failing-test_harness-v7-orchestrated_r1_20260806T073835Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v7-orchestrated` @ `83298cad` | fail | reasoning | 9,734 |
| `retry-after-case_fix-from-failing-test_harness-v7-orchestrated_r2_20260806T073921Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v7-orchestrated` @ `83298cad` | fail | reasoning | 16,936 |
| `retry-after-case_fix-from-failing-test_harness-v7-orchestrated_r3_20260806T074008Z` | `retry-after-case` / `fix-from-failing-test` | `harness-v7-orchestrated` @ `83298cad` | fail | reasoning | 10,958 |
| `retry-after-case_fix-from-failing-test_session_r1_20260821T100622Z` | `retry-after-case` / `fix-from-failing-test` | `session` @ `d48215d8` | pass | — | 21,032 |
| `stale-categories_session-from-notes_context-and-gate_r1_20260820T214302Z` | `stale-categories` / `session-from-notes` | `context-and-gate` @ `710447ea` | pass | — | 91,750 |
| `stale-categories_session-from-notes_session_r1_20260820T214135Z` | `stale-categories` / `session-from-notes` | `session` @ `d48215d8` | pass | — | 100,812 |
| `stale-categories_stale-categories_session_r1_20260820T214431Z` | `stale-categories` / `stale-categories` | `session` @ `d48215d8` | pass | — | 128,314 |
| `threshold-off-by-one_session-from-notes_context-and-gate_r1_20260820T212940Z` | `threshold-off-by-one` / `session-from-notes` | `context-and-gate` @ `710447ea` | tampered | — | 55,834 |
| `threshold-off-by-one_session-from-notes_context-and-gate_r1_20260821T093203Z` | `threshold-off-by-one` / `session-from-notes` | `context-and-gate` @ `4c24a546` | timeout | stopping | 437,848 |
| `threshold-off-by-one_session-from-notes_deepagents_r1_20260826T063159Z` | `threshold-off-by-one` / `session-from-notes` | `deepagents` @ `2dd3285f` | tampered | — | 0 |
| `threshold-off-by-one_session-from-notes_deepagents_r1_20260826T071514Z` | `threshold-off-by-one` / `session-from-notes` | `deepagents` @ `614bbc8d` | timeout | stopping | 0 |
| `threshold-off-by-one_session-from-notes_deepagents_r1_20260826T074701Z` | `threshold-off-by-one` / `session-from-notes` | `deepagents` @ `614bbc8d` | timeout | stopping | 0 |
| `threshold-off-by-one_session-from-notes_deepagents_r1_20260826T091644Z` | `threshold-off-by-one` / `session-from-notes` | `deepagents` @ `8432dcf0` | tampered | — | 0 |
| `threshold-off-by-one_session-from-notes_deepagents_r1_20260826T103510Z` | `threshold-off-by-one` / `session-from-notes` | `deepagents` @ `78713af4` | tampered | — | 0 |
| `threshold-off-by-one_session-from-notes_harness-v8-session_r1_20260807T082354Z` | `threshold-off-by-one` / `session-from-notes` | `harness-v8-session` @ `8311b5bb` | crash | stopping | 123,774 |
| `threshold-off-by-one_session-from-notes_harness-v8-session_r2_20260807T083455Z` | `threshold-off-by-one` / `session-from-notes` | `harness-v8-session` @ `8311b5bb` | pass | — | 153,786 |
| `threshold-off-by-one_session-from-notes_session_r1_20260820T212922Z` | `threshold-off-by-one` / `session-from-notes` | `session` @ `d48215d8` | crash | stopping | 2,422 |
| `threshold-off-by-one_session-from-notes_session_r1_20260821T092959Z` | `threshold-off-by-one` / `session-from-notes` | `session` @ `d48215d8` | fail | reasoning | 120,666 |

# Authorship: independent test author B (job 0028, D-2a)

Independent test author B wrote these files. Author B is a separate, clean-context Claude agent (model Claude Opus 5.5, `claude-opus-5-5`), dispatched on 2026-10-15 after the API contract (commit 5fbe9fd) and the golden fixture (commit cc0da88) were committed on branch `d2a-0028`, worktree `topo-pilot-d2a`. Every file was written before the author saw any module source, using only the frozen protocol and `tools/d2a/API.md`. The author is not the implementer.

| File | Lines | Test functions | Protocol test ids |
|---|---|---|---|
| `test_b_targets.py` | 211 | 14 | T-BETA: `beta`, `band_edge_table`, β₂ on oracle decision contrasts |
| `test_b_rules_flags.py` | 292 | 25 | T-RULES: `learned`, `stage1_decision`, `arm_value`, `carries`, `low_increment`, `beta2_pass`, `precision_ok`, `c_hor`, `c_len` (ruling D1), `pipeline_null_ok` (ruling D3) |
| `test_b_rules_decide.py` | 319 | 26 | T-RULES: `decide`, rules 1–10 in order, rule-4 combinations, rule-5 matched seeds, missing-seed convention, UNRESOLVED C-HOR |
| `test_b_rules_qualifiers.py` | 231 | 13 | T-RULES: qualifiers (LENGTH, PRECISION_LIMITED, WORLD_CONDITIONAL_CEILING, CAVEAT_REREAD, BEHAVIOUR), none for outcomes 1–3 |
| `test_b_resource.py` | 366 | 20 | T-RESOURCE: `verify_identity`, `bind_meter`, `Supervisor`, `admit`, `stage_spent`/`total_spent`, `disk_reason`, `boundary`/`D2AStop`; `Limits`, `RUNS`, `WAVES`, `TRAIN_CFG`/`MODEL_CFG` |
| `test_b_behaviour.py` | 148 | 12 | §9.3 `pair_scores`; §7.4 `shuffle_perm` |

With parametrisation, 585 tests were collected at job 0028. The correction round below adds six parametrised cases (591, counted by hand; pytest was not run in that round).

## What was read

- **The contract, in full:**
  - `agent-handoff/planning/responses/D2A-FROZEN-v1.md`, all 1,127 lines;
  - `tools/d2a/API.md`.
- **Production code the tests call or that the API reuses** (read-only):
  - `tools/d1_seam/d1_seam.py`: lines 1–36, 80–95 and 116–148, plus a grep of its top-level names;
  - `src/topo_pilot/oracle`: `__init__.py`, `_filter.py` lines 14–80, `_futures.py` lines 15–62, and `as_model` in `_common.py`;
  - `src/topo_pilot/contracts/errors.py`, lines 1–80;
  - `ModelConfig` and `TrainConfig` in `src/topo_pilot/learner/config.py`;
  - the import lines of `learner/__init__.py` and `dataset/__init__.py`;
  - grep only: the `SeedTree` method lines in `contracts/ids.py`, and the exports in `contracts/__init__.py`.
- **The meter modules** in `tools/x4_oracle_profile`:
  - `controls.py`, in full;
  - `meter.py`, lines 1–58 and 175–260, plus a grep of its top-level names;
  - `winjob.py`, a grep of its top-level names.
- **For style and format:**
  - the first 40 lines of `tests/d1_seam/test_d1_seam.py`, and `tests/d1_seam/AUTHORSHIP.md`;
  - `tests/c1prime/AUTHORSHIP_B.md`, and the first 30 lines of one `tests/c1prime/test_b_*.py`;
  - the pytest and ruff sections of `pyproject.toml`.

## Deviations (reads outside the dispatch's MAY list; all read-only)

- `d1-seam-oracle-store/d1_meter_bind.py`, because the protocol names it as the pattern for the store-local meter binding (§11.1, §11.3). The fake meter namespaces copy its attribute names.
- The real mailbox's `agent-handoff/request.json` and `agent-handoff/jobs/0028/task.json`, so the synthetic mailbox would copy their field layout. Nothing under `agent-handoff` was written or modified. The tests build their own mailbox under `tmp_path`.

## What was not read

- **No `tools/d2a/*.py`.** A directory listing at the start showed only `API.md`. No module source was opened, grepped or imported for viewing.
- **Not `src/topo_pilot/learner/multihorizon.py`.** Its name appears in `git status`; it was not opened.
- **None of author A's files.** That covers `tests/d2a/test_a_*.py`, `AUTHORSHIP_A.md` and `tests/learner/test_multihorizon.py`.
  - Their names were seen in `ls` and `git status` listings.
  - Once, a pytest run given the directory `tests/d2a/` printed the collection-error line `ERROR tests/d2a/test_a_world.py`. Nothing else of those files was shown or opened. Every later run named author B's files explicitly.
- **No temporary or scratch areas:** nothing under `C:/Users/pc2/AppData/Local/Temp/claude/`, and not `tmp-0028/a_check*.py` (names seen in a listing only).
- **No stores and no other worktree.**

## What was executed (disclosure)

The venv Python (`topo-pilot/.venv`) was run with `PYTHONPATH=topo-pilot-d2a/src` and `TEMP`/`TMP` set to `tmp-0028`, and with no bytecode or pytest cache written.

1. **A self-check of the tests' own logic.**
   - Throwaway fakes of `d2a_decide`, `d2a_targets`, `d2a_eval` and `d2a_train` were written from this author's reading of the protocol, in `tmp-0028/authorB_selfcheck/`.
   - A pytest plugin preloaded them into `sys.modules`, so no real `tools/d2a` module could be imported.
   - All 585 tests passed against the fakes.
   - 24 single-line mutations of the fakes were then run. Each one targeted a trap: ≥ vs >, matched seeds, an UNRESOLVED C-HOR, the window prior, p = 33, the kill scope, `controls.MAILBOX` rebinding, the disk floor, strict resolution, HOLD sleeping, and the rule-4 branch. Every mutation was killed after one test was strengthened: absolute resolution now checks each member separately.
   - The fake directory was then deleted. It is not an implementation and was never placed in the repository.
2. **`ruff check --fix`**, on the six author-B files only, named one by one. It fixed import ordering only. No `ruff format` was run.

The total CPU used was well under a minute. No git command that writes was run, and nothing was committed.

## Ambiguities found, and how the tests resolve them

1. **`learned()` and `None` (the most important).** The API says "`None` (missing or INVALID model) → FAIL", but `beta()` returns `None` for an undefined slope.
   - *Resolved by ruling Q6 (d2a-0029).* A missing or INVALID model is now passed explicitly as `model_status="MISSING"` or `"INVALID"`, and gives `"FAIL"`. Four `None`s with the default status (a present model) give `"UNRESOLVED"`.
   - The job-0028 tests had taken `learned(None, None, None, None) == "FAIL"` as the missing-model convention. That expectation was wrong: the old signature gave no evidence that the model was missing.
   - A single `None` among defined values must give `"UNRESOLVED"`. That is §6: an undefined statistic of a present model is never a defined FAIL. A NaN in any slot also gives `"UNRESOLVED"`.
2. **Undefined values in the flag functions.**
   - `low_increment(NaN)` is False. An undefined increment fails every per-seed condition (§10.5); the API names only `None`.
   - `c_len` with a NaN per-seed value gives `LENGTH_UNRESOLVED` (§10.4, "defined score"); the API names only `None`. Ruling 6b (d2a-0029) confirms this and extends it to a NaN mean or interval endpoint, now tested too.
   - `c_hor` gets the same treatment, as the API says ("None or undefined").
3. **`pipeline_null_ok` keys.** The tests use the keys `("d2a-s1-N", 16)`, `("d2a-s1-N", 28)`, `("d2a-s2-N", 16)` and `("d2a-s2-N", 28)`. The function's verdict must not depend on how the keys are spelled. A dict with only three keys gives False ("all four are defined").
4. **The `decide()` result format.**
   - The `"rule"` field is read as its leading integer, so `4`, `"4"` and `"4b"` all read as 4.
   - `BEHAVIOUR(H, t)` is matched by its prefix and its two integers, so `BEHAVIOUR(H2,28)` and `BEHAVIOUR(H2, 28)` both work.
   - Qualifiers are compared as sets.
5. **No qualifiers for rule 3 (PIPELINE_INVALID).** API.md mentions only rules 1–2, but §1.4 attaches qualifiers to outcomes 4–10 only, so the tests expect none for rule 3.
6. **PRECISION_LIMITED scope.** *Corrected by ruling 6a (d2a-0029).* §10.5 scopes the qualifier to "any model entering the rule that fired"; the job-0028 tests had wrongly applied the API's "any H1 or H2 model" to every outcome from 4 to 10.
   - Rule 8 (PREDICTIVE_WITHOUT_LINEAR_POSTERIOR) conditions only on H2 models. An H1-only precision failure leaves the qualifier absent; an H2 failure adds it.
   - Rules 4 (MULTISTEP_ENABLES_LEARNING), 5, 6 and 7 involve both H1 and H2 models, so a failure in either arm adds it.
   - Rule 9: a precision failure in any H1 or H2 model gives INCONCLUSIVE with the qualifier, unchanged.
   - Still a reading, not a ruling: rule 10 (INCONCLUSIVE from `base()`) is treated as involving both arms. It is reached only after rules 5–9, all of which involve H1 or H2 models, and rule 9's own precision condition covers every H1 and H2 model.
   - The qualifier never changes the outcome, except that outcome 9 becomes INCONCLUSIVE.
7. **CAVEAT_REREAD counting.** Its two conditions are counted separately (≥ 3 seeds each), not as matched seeds, as §10.5 writes them.
8. **`band_edge_table` return type and row order.**
   - The result may be a dict with the keys `ep`, `p`, `d`, `r8` and `rm`, or a tuple in that order.
   - Row order is not assumed; rows are sorted by `(ep, p)` before comparison.
   - The tests expect `rm` from `q_model[row, p]`; one test checks that a model shifted by one index fails.
9. **`Supervisor.check` reasons.**
   - A reason may be a string or a mapping. Its status is the value that starts with `INCOMPLETE:`.
   - `polling_interval_s` must be a mapping key, or appear in the string.
   - Not tested: which reason wins when the stage and total budgets are both exceeded, or when one check combines a per-child kill with a budget overrun.
   - Equality with a limit does not kill (the API's ">").
10. **`bind_meter` file names.**
    - `LEDGER`, `LOCK` and `LOG_DIR` must be `cpu_ledger.json`, `RUN.lock` and `logs` under `out` (API §5 store layout).
    - `EMERGENCY` and `ACTIVE` need only lie under `out` and differ from the other paths, because the API does not name them.
    - "Exactly the §11.3 names" is read strictly. No module attribute may be added, and none outside the list may change. Rebinding `controls.MAILBOX`, for example, fails the test.
11. **`verify_identity`.**
    - Digests are uppercase hex, as in the real mailbox. The return value is not checked, and neither is the `check` string of the `StageFailure`; only `code == INVALID_CONFIG` is.
    - A missing `RUN.lock` must raise something (fail closed); the exception type is not checked.
    - Each rejection case changes exactly one identity. A second, valid job directory, `0029`, exists, so the request's `job_id` is the only thing that fails.
12. **`disk_reason`.** The fake `usage(path)` answers by the drive letter of its argument. A healthy result must have queried both C: and X:.
13. **`admit`.** A remaining budget exactly equal to `need_s` is admitted (the API says "below").
14. **`beta`.** A tiny positive Σd² (10⁻²⁰⁰) is defined; an overflow to inf (d = 10²⁰⁰) is UNDEFINED. Both follow the API's "not positive and finite" exactly. A tolerance-based cutoff would fail.
15. **`pair_scores` (an observation, not a defect).** The result is read as a mapping with the API names `Delta`, `E_contrast`, `tv_pred`, `reproduced` and `abs_resolved`.
    - Given E_contrast ≤ 0.5, the triangle inequality already forces 0.5Δ ≤ tv_pred ≤ 1.5Δ. The band's boundary cases therefore always coincide with E_contrast = 0.5 exactly.
    - Both boundaries are tested as reproduced, and the values just beyond them as not reproduced.
16. **`WAVES` / `RUNS`.** Values are compared as tuples, including the order within each wave (§4.7). `TRAIN_CFG` and `MODEL_CFG` are compared by dataclass equality. `THREADS` is not tested, because its representation is unspecified.

## Correction round (job 0029 pre-dispatch)

The same author role, in a new clean-context Claude Opus 5.5 session, made these corrections on branch `d2a-0028` (from HEAD 0b691bc). They follow the coordinator rulings in `agent-handoff/planning/responses/d2a-0029-rulings.md` and the Codex rulings `coord-d2a-0029-rulings-20261015.codex.md`. The S6 change follows `D2A-FROZEN-v1.coordinator-addendum-1.md` (owner addendum 5).

| Change | File | Ruling |
|---|---|---|
| Four `None`s give `UNRESOLVED`; `model_status="MISSING"` and `"INVALID"` give `FAIL`. The single-`None` tests are kept. | `test_b_rules_flags.py`, `test_learned_four_none_is_unresolved_unless_model_status_says_missing_or_invalid` | Q6 (Codex 1) |
| A NaN mean, 1.25th or 98.75th percentile gives `LENGTH_UNRESOLVED`, on both the GAIN and LOSS bases. The missing-input and NaN-seed tests are kept. | `test_b_rules_flags.py`, `test_c_len_nan_mean_or_interval_endpoint_is_unresolved` | 6b |
| The PRECISION_LIMITED expectations are split by firing rule: both arms for rules 4–7 and 10; H2 only for rule 8. The rule-9 test is unchanged. | `test_b_rules_qualifiers.py`, `test_precision_limited_on_h1_or_h2_failure_when_both_arms_enter`, `test_precision_limited_on_rule8_counts_only_h2_models` | 6a |
| `Limits` now expects per model 7 CPU-h; stages 2/2/14/84/12 CPU-h; total 114 CPU-h. In `test_admit`, the stage-1 rows move from 25,000 to 50,200 s spent, so 200 s remain, as before. The total rows move to `114 * HOUR - 100.0` / `- 150.0`. | `test_b_resource.py`, `test_limits_defaults_are_the_s6_values`, `test_admit` | Q3 (Codex 3) with owner addendum 5 |
| Ambiguities 1, 2 and 6 above are rewritten. | `AUTHORSHIP_B.md` | Q6, 6a, 6b |

- **Wave arguments.** `test_b_resource.py` asserts no wave `--max-cpu`/`--max-wall` values. None were added, because there is no existing API name to assert them through.
- **What was read in this round:** the three rulings/addendum files in full; D2A-FROZEN-v1 lines 775–830 only (§10.4–§10.5); author B's own test files; and a grep of `tools/d2a/API.md` for `max-cpu`/`wall`. No `tools/d2a/*.py`, `multihorizon.py` or author-A file was opened.
- **What was executed:** `python -I -m py_compile` on each changed test file. Edits were made as bytes, which kept the LF line endings. No pytest run, and no formatter.

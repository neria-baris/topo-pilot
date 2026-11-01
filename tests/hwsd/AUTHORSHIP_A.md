# Author A (job 0197): what was read, what was written, coverage

**Role.** Independent test author A, estimand and statements side, clean-context Claude subagent of coordinator d9a66698, 2026-11-01. Job file `agent-handoff/jobs/0197/task.md` (sha256 efe97bcd…2c4ad4c, verified) and `RULINGS_PHASE1.md`.

## Read

- **The spec (commit 76fd85e):**
  - `tools/hwsd/PROTOCOL_HWSD_v1.md` (sha256 938cebd5…7775, verified);
  - `tools/hwsd/API.md` (89ff369f…);
  - `tools/hwsd/CONTRACT.json` (fb350da6…);
  - `tools/hwsd/TEST_PLAN.md` (15d7e432…).
- **Reused modules, public APIs only:**
  - `tools/k4b/API.md`: chart, scores, cert, stats and decoder rows;
  - `tools/c1prime/API.md`: §6 `c1_means` and §3 `c1_chart` (ledger, `c0_val`);
  - `tools/hwsb/API.md`: `hwsb_eval` rows and `kb6`;
  - `tools/hwsc/API.md`: `status_of` and the exception conventions.
- **Signatures and docstrings,** printed by an AST script, never whole bodies:
  - `k4b_stats`: `model_status`, `bounds`, `joint_bootstrap`;
  - `k4b_cert`: `isqrt_bracket`, `norm_bound`, `b_num`, `margin`, `F_plan`, `certify`;
  - `k4b_config`: the constants and `check_chart_equality`;
  - `k4b_scores`: `m4_phase`, `oracle_phase`, `phase_scores`, `endpoint_arrays`, `naive_scores`;
  - `c1_means`: `rank_for`, `bootstrap_means`, `quantile_with_rank`, `rank_check`, `tree_mean`;
  - `hwsb_eval`: `b1`, `forcing`, `model_predictive`, `oracle_predictives`;
  - `hwsb_config.Z_B23`;
  - `c1_records.C1GateFailure`;
  - `c1_chart.ConstructionLedger` and `c0_val`;
  - `k4b_charts.build_chart` and `extend`.
- **Short reused-code excerpts:**
  - `tools/x4_circle_history/scores.py`: `unit_vectors`, `scores`, `r4_norms` (a few lines);
  - `tools/hws/hws_oracle.kl_rows`: its first lines, seen in a test traceback;
  - `hws_worlds.HwsStop` (class header);
  - the `LearningGate` docstring in `src/topo_pilot/prediction/metrics.py`;
  - `pyproject.toml` `[tool.pytest.ini_options]`.

## Not read

- **Code under test.** No `tools/hwsd/*.py` was opened, listed for content or searched. `git status` showed some file names.
- **Author B's tests.** No `tests/hwsd/test_b_*` and no `AUTHORSHIP_B.md`.
- **Other tests.** No `tests/hwsc`, `tests/k4b` or `tests/hwsb` code.
- **Public summary.** Neither public-summary path (`00_READ_ME_FIRST*`, `docs/research_summary/`).
- **Track U.** No file of track U.
- **Blinded paths.** Nothing under `hwsc-store/stages/TRAIN/**`, `hwsc-store/logs/**`, `topo-scratch/hwsc-job-*`, `jobs/0187|0188|0189/review.md`, `stages/E1/L1.json`.
- **Store files.** No store file of any kind, and no payload or array.

## Method

- **The oracle.** `test_a_hwsd_ref.py` is a separate reference reading of protocol §5, in pure Python with exact `Fraction`s. Its own tests pin it to the API.md §17.3 KD4 table. Other files compare `hwsd_statements` with it, both on hand-derived fixtures and on 400 random planted tables per file.
- **No self-oracle.** Expected values never come from the function under test. Pass-through checks use the reused functions (`hwsb_eval.b1`/`forcing`, `c1_means.bootstrap_means`, `k4b_cert.b_num`/`margin`, `k4b_scores.endpoint_arrays`/`control_arrays`) as their public APIs document them.
- **Debugging the tests.** Before committing, I ran the tests against throwaway stand-ins I wrote myself from API.md alone. They live in my scratchpad and are not committed. Eight rule mutants in the stand-in statement logic were all detected, among them strict versus non-strict inequalities, the k_C > k_L split, the D6 k1 < K rule, CHART_AT_INIT, NEVER and k_C⁺.
- **Placement.** Every write goes to pytest `tmp_path`, under `--basetemp X:/Downloads/topo-scratch/test_hwsd-0197/…`. No formatter was run.

## Files and coverage (TEST_PLAN §2 rows)

| File | Tests | TEST_PLAN row / protocol items |
|---|---|---|
| `test_a_hwsd_ref.py` | 3 | the reference and its self-checks (API.md §17.3, K4B §8.1 boundaries) |
| `test_a_known_bound.py` | 13 | **KD6** (run by `dk.kd6`; every check inside `db.bound_hwsd()`):<br>(1) Proposition 1 by exact enumeration (2–3 states, 2–3 symbols, L = 6, K = 4; a whole-history field is non-zero);<br>(2) Theorem A over completions;<br>(3) Lemma N `isqrt_bracket` and `norm_bound`, exact;<br>(4) `model_status` boundaries at M = 1/100 (equality, UNRESOLVED/NUMERICAL, NEGATIVE_ALIGNMENT, one-ulp) plus a 2,000-point grid;<br>(5) ranks 84/4,917/125/4,875/250 and 70/49,931, `bounds` ranks;<br>(6) chart equality and protocol sha inside the binding;<br>(7) MODELS restored |
| `test_a_bounds.py` | 11 | **test_a_bounds**:<br>`strong_bounds` against an `np.sort` index (69, 49,930), with NaN, inf and length 5,000 → NUMERICAL;<br>`main_bootstrap` = `c1_means.bootstrap_means(…, 620413, 5000)`, its default seed inside the binding, and the index stream independent of the other arrays;<br>`strong_bootstrap` seeds 620416 / dry 629965, 50,000 draws, X± keys (spy; slow: bitwise and seed-sensitive);<br>`f_sides` planted and certified;<br>`bootstrap_inputs_d` order and values;<br>the constants |
| `test_a_onsets_order.py` | 48 | **test_a_onsets_order**:<br>`est`/`ok`/`sigma`;<br>strict equality of `above_s`/`below_s` (exact 1/100 and `nextafter`);<br>onsets k_C, k_C\*, k_C⁺, k_L, k_P (strict), k_B, k_B^S, including undefined, SCORED_UNVALIDATED never an onset, UNCERTIFIED valid counting for k_C, and a chart lost after k_C;<br>`n_pre`/`pre_chart_max`, including k_C undefined;<br>ORDER at both anchors for every category, including BEFORE over a NA anchor, LEARNING_BEFORE_CHART vs UNCERTIFIED_AT_ANCHOR, FINAL_NA vs UNRESOLVED, and UNRESOLVED/NUMERICAL;<br>explicit A (k_C⁺);<br>the onset-order line;<br>the random cross-check |
| `test_a_statements.py` | 27 | **test_a_statements**, per model and aggregate:<br>D1, every reading;<br>D2: CHART_AT_INIT first, NO_CHART, FALSE (also with a final not SUPPORT), FINAL_NOT_SUPPORT, TRUE INFORMATIVE/UNINFORMATIVE with the exact boundary, BY_CONSTRUCTION in 1/2/3 models, UNINFORMATIVE_PRE_CHART, F-2;<br>D3 RC-4;<br>D4, every reading;<br>D5, every reading;<br>D6 on OK rows only, the EST-only diagnostic (S3), vacuous, k1 < K;<br>the generic aggregate rule;<br>the reasons are CONTRACT reasons;<br>the random cross-check |
| `test_a_evaluate.py` | 11 | **test_a_statements** (rest):<br>`evaluate` structure and values;<br>`headroom_ok`/`resource_ok`, with RESOURCE before HEADROOM;<br>any K;<br>`diagnostics`: mc, positive, `chart_at_init`, `est_loss`;<br>`fill_templates`: CONTRACT texts, the D4 second sentence, D3_CHART_AT_INIT, missing → n/a;<br>`outcome_d` precedence |
| `test_a_scorer.py` | 19 | **test_a_scorer**:<br>`checkpoint_dir`/`ledger_for` (one file per checkpoint);<br>`chart_one` order with spies: production before direct, val activations only after FROZEN.json, FROZEN contents and hashes, a second claim refused, a C0-CAL failure giving no direct claim, decoder or freeze, `skip_direct`, direct not PASS, FAIL_TECHNICAL stops;<br>`status_of_checkpoint` for every label format and precedence;<br>`map_build` (row 9);<br>36 checkpoints → 72 claims, 36 ledgers;<br>`arrays_one(planted=True)`;<br>`controls_one` = `control_arrays` bitwise, with the decoder unavailable |
| `test_a_learning.py` | 11 | **test_a_learning**:<br>p = q32 → captured 1; q1 → 0; q4 → d̄ = 0 and L ≤ 0;<br>exactly 0.8 passes (a planted exact case);<br>pass-through of `b1`/`forcing` at z and z_S;<br>G_C ≈ 0 and NaN → NUMERICAL;<br>Z, Z_S;<br>`dk.kd5()` (slow) |
| `test_a_kd4.py` | 17 | **test_a_kd4**:<br>`plant_acts` cases (i)–(v) against an independent construction (`u(id)`, the g map, noise and seeds), the case-(iv) mass and monotonicity;<br>the six §17.3 sequences on planted rows (AFTER, WITH, BEFORE, NEVER, NO_CHART, the step-0 control CHART_AT_INIT) through `evaluate`, with σ at step 0 and k_C⁺;<br>`seq_cases` end to end (slow; skipped while the KD4 parameters are TO_FREEZE unless `HWSD_KD4_PARAMS` is set) |

**Totals.** 160 tests, of which 3 are marked slow (`test_strong_bootstrap_bitwise_and_seed_sensitive`, `test_kd5_passes_on_w0`, `test_seq_cases_end_to_end`). They fail at import until `tools/hwsd` lands; that is expected.

## Markers in the code

- `# SPEC-QUESTION:` marks:
  - the archived-wall label (`test_a_scorer.py`);
  - the KD4 parameter location before the freeze (`test_a_kd4.py`).
- `# API-AMBIGUITY:` marks:
  - the `seq_cases` result layout;
  - the `c0_val` criteria as a dict;
  - the layout of `scores[...]["arrays"]`;
  - the form of `evaluate`'s order entries;
  - the exact-0.8 skip.

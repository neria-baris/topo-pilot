# K4b test plan v1 (job 0045)

Authority: `tools/k4b/PROTOCOL_K4B_v1.md` §11.3 field 5, §11.4, §6 (S0, PF). Functions are those of `tools/k4b/API.md`; constants are in `tools/k4b/CONTRACT.json`. The protocol wins on conflict.

## 1. Rules

- Two clean-context authors, A and B. They work only from the frozen protocol, `API.md`, `CONTRACT.json`, this file, `CERTIFICATE.md` and the reused frozen code (§11.3). They **never read, list or search `tools/k4b/*.py`**, and execute nothing.
- Files: author A writes only `tests/k4b/test_a_*.py`; author B writes only `tests/k4b/test_b_*.py`. `tests/k4b/AUTHORSHIP.md` records what each read and did not read.
- The tests are committed before any module enters the worktree, A then B, as separate commits. Only a file's own author may correct it.
- **No formatter is ever run over `tests/k4b`.**
- Tests are synthetic. They open no store payload, sample no scientific history, load no checkpoint and run no stage. Synthetic stores, registries and mailboxes live under pytest's `tmp_path` (`--basetemp` on X:).
- Import: `sys.path` gets `<repo>/tools/k4b` (plus the reused-module directories, as `k4b_config` does). Modules are imported by name (`import k4b_cert`).
- Exact arithmetic for every certified quantity: `fractions.Fraction`, integers.

## 2. Author A: mathematics and certificate

| # | Item | Target |
|---|---|---|
| A1 | Proposition 1 by exact Fraction enumeration on a tiny asymmetric stationary HMM (L = 6, K = 2): E[g(S_K)·r_K] = 0 for random suffix tables g; ≠ 0 for a prefix-dependent g | protocol §1.2 (self-contained exact code) |
| A2 | Theorem A on that HMM with a support set correlated with the prefix and the residual sign: every completion on a grid and the extremal ones lie in [E X−, E X+]; sharpness; the continuity path; conditioning on S gives a spurious non-zero value while the bounds stay valid | §1.4; `k4b_scores.endpoint_arrays` for the row construction |
| A3 | Lemma N against exact rationals, including s = 0, tiny values and adversarial n̂ | `k4b_cert.isqrt_bracket`, `norm_bound` |
| A4 | Lemma T on a toy perturbation with a known κ | CERTIFICATE §2 (exact toy) |
| A5 | `row_bound` at K = 1 and 2 | `k4b_cert.phase_bound`, `envelopes` |
| A6 | B_num and decision boundaries: L − F exactly 0.01 is not SUPPORT; U + F exactly 0.01 is not EXCLUDE; the lower side exactly at −0.01; NEGATIVE_ALIGNMENT; UNRESOLVED/NUMERICAL; SUPPORT and EXCLUDE exclusive; the overall outcome table | `k4b_cert.b_num`, `margin`; `k4b_stats.model_status`, `overall` |
| A7 | Ranks 84, 125, 250, 4,875, 4,917 | `k4b_config.RANKS`; `c1_means.rank_for`; `k4b_stats.bounds` |
| A8 | The cap: 1e-4 passes and the next value above fails; P2 analogue | `k4b_cert.cap_ok`, `p2_ok` |
| A9 | Ladder projection on synthetic arrays: invariance to mean shifts; the joint count threshold 4,000 of 5,000; UNDERPOWERED | `k4b_stats.projection`, `ladder`, `mde_ok`, `centered` |
| A10 (v2) | Directional error-rate counterexample of RC1, analytically specified (zero-width, E X− = E X+ = 0.01, enumerable law of the two one-sided bounds): false-SUPPORT and false-EXCLUDE are disjoint opposite-tail events; combined probability = their sum, exceeds each, ≤ 2α when each ≤ α. Exact arithmetic; not a simulation-enforced bound | §8.3; `k4b_stats.model_status` for the events |
| A11 (v2) | Deterministic F_plan: B_constant(1e-4, 4, 12288) against exact rationals; F_test ≤ F_plan whenever the cap and |X̂| ≤ 4 hold for n ≤ 12,288 | `k4b_cert.F_plan`, `b_num`, `margin` |
| A12 (v2) | Width-preserving diagnostic of §7.6 on synthetic arrays: invariance to C̄; the D̄ shift | `k4b_stats.width_diagnostic` |
| A13 | B4 guard: PASS, HEADROOM, NUMERICAL band; FRESH_B4_LOW | `k4b_cert.b4_guard` |

## 3. Author B: data, chart reuse, registry and flow

| # | Item | Target |
|---|---|---|
| B1 | Seed streams and fixed 3,072-row blocks (content invariant to k); IDs; int-keyed maps | `k4b_data.history_generator`, `sequence_ids`, `sample_block` (synthetic T/E/π), `k4b_config.require_int_keys` |
| B2 | Registry with C1′-style digest columns, a D-2a-style raw-token store and a NOT_SCANNED entry | `k4b_registry.source_d`, `source_e`, `inventory`, `classify`, `build` on a synthetic root |
| B3 | Every collision → FAIL_TECHNICAL/LINEAGE; within-split duplicates kept | `k4b_data.separation_cal_val`, `separation_fresh`, `seq_disjoint`, `duplicates` |
| B4 | `c1_chart` called with the K4b cfg (cfg equality) | `k4b_config.chart_cfg`, `check_chart_equality` |
| B5 | Two ledgers (6 trained, 3 step-0; "direct" refused on step-0) | `k4b_charts.open_ledgers`, `InitLedger` |
| B6 | Valid step-0 INCONCLUSIVE/CHART_UNAVAILABLE is non-gating and recorded INIT_UNAVAILABLE; FAIL_TECHNICAL in shared chart code or shared integrity machinery stops immediately | `k4b_charts.init_charts` (with monkeypatched chart kernels) |
| B7 | Production chart and decoder frozen before any validation activation; no gauge or refit on validation or test | `k4b_charts.freeze_production`, `require_frozen`, `c0_val_gate` |
| B8 | GIANT 487 passes and 486 fails; support 507 passes and 506 fails | `c1_chart.giant_pass`; CONTRACT chart values; `c1_chart.c0_val` via `k4b_charts.c0_val_gate` |
| B9 | The sealed file | `k4b_stats.write_sealed`, `check_unsealed`, `SEALED_KEYS` |
| B10 | Gate order and first-non-PASS stop | `k4b_driver.GATE_ORDER`, `run_gates` |
| B11 | No fresh access without release B | `k4b_fresh.require_release_b`, `k4b_release.verify_release` |
| B12 | The determinism recheck | `k4b_charts.determinism_check` |
| B13 | Rerun rule of §11.8: superseded moves, hash restore, refusal on unrecorded prior files | `k4b_release.archive_attempt`, `restore_records`, `lineage_ok` |
| B14 (v2) | Reconstruction of sealed means refused: a validation report allowing X̄± = C ± D is refused; no supported contribution or conditional supported mean in it | `k4b_stats.check_unsealed`; `k4b_scores.support_report(..., sealed=True)` |
| B15 (v2) | Malformed handoff JSON → INCONCLUSIVE/REGISTRY_INCOMPLETE, never an empty contribution | `k4b_registry.validate_handoff_json`, `source_c` |
| B16 (v2) | Non-default registry roots: `observation_set_sources` with a non-default root and a matching explicit store reads that root, not main's artifacts | `k4b_registry.source_a` |
| B17 (v2) | Sealed-D-2a predicate: a history in {0,…,4}³² → INCONCLUSIVE/REGISTRY_INCOMPLETE; no sealed token array is opened | `k4b_data.sealed_d2a_predicate`, `predicate_check`; `k4b_registry.source_e` |
| B18 (v2) | Interrupted-stage replay: no terminal gate record; archive and byte restore; bit-identical regeneration; owner escalation rules (changed or at/after-failure outcome-bearing quantity → owner; unchanged before the point → not by itself) | `k4b_release.archive_attempt`, `restore_records`, `regenerated_identical`, `needs_owner` |
| B19 (v2) | Actual meter bindings: controls, meter, winjob values after `bind`; `--max-cpu inf --max-wall inf`; op_guard deadline per operation; child TEMP/TMP/TMPDIR on X:; worker session and RUN.lock identity from the release | `k4b_meter_bind.bind`, `rewrite_argv`, `child_env`, `main` (argument handling only) |
| B20 (v2) | Simultaneous overdue-operation/disk conditions with STOP and INVALID: control reason and state keep precedence. HOLD with and without a resource failure; latch processing preserved and the HOLD state returned. Ordinary overdue and disk failures, including unreadable free space | `k4b_meter_bind.make_limiter`, `disk_reason`, `classify_stop` (with a fake legacy and a fake clock) |
| B21 (v2) | G0 seed classification (RC5): K4b's own declarations are not prior use; an unclassified hit fails closed | `k4b_driver.classify_seed_hits` |

## 4. Regression and preflight (PF, job 0046)

Unchanged suites: `tests/circle_history`, `tests/c1prime`, `tests/c1prime_registry`, `tests/oracle_profile`, `tests/oracle`, `tests/dataset`, `tests/contracts`, `tests/prediction`, `tests/analysis`, `tests/experiment`, `tests/learner`; the new `tests/k4b`; `tools/check_file_sizes.py`. `tempfile.gettempdir()` inside a metered child is on X:. The C1′ suite takes about 12 minutes and is run detached.

## 5. S0 (at the freeze commit)

`k4b_release.pin_check(repo, R_ref, H_exec)`: only `A` entries under `tools/k4b/` and `tests/k4b/` across the protected paths of CONTRACT `s0`; every `reuse_sha256` and `protected_sha256` value equal; C1′ CONTRACT chart section equal to R_ref; GAP doc blob sha256 8b5c7049…f091.

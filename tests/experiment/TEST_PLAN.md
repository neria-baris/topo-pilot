# TEST_PLAN: experiment

Marker: `pytest.mark.experiment`. Uses stub stages and gates (no science). Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| X01 | Config layering base → stages → local; the resolved hash is stable; changing a closed key after S2 raises `CONFIG_DRIFT` | contract |
| X02 | A stage with a failed required gate raises `GATE_FAILED`; `--waive` without `--reason` is rejected; a waiver is recorded in the manifest | error path |
| X03 | `RunPlanner.ordered_runs("S4")` equals the exact order in STAGES §2 | known answer |
| X04 | `ReportBuilder` reads only MetricRecords, GateReport, and RunManifest (spy on the store) and marks missing stages "not run", never 0 | contract |
| X05 | Report sentence templates: each F1 verdict selects the right template; INCONCLUSIVE includes the reason | known answer |
| X06 | `status` output stays within 40 lines on a store with 100 artifacts | contract |
| X07 | `prereg` writes all closed decisions and the S2 tables; it refuses if S2 gates have not passed | contract |
| X08 | `x4c_category` for the four status combinations (and INCONCLUSIVE counting as not supported); `run_rule_verdict`: all runs ≥ min → SUPPORTED; one run below → REJECTED; a gate False/None → INCONCLUSIVE; 2 of 3 replicates → INCONCLUSIVE; exactly min passes | known answer |
| X09 | `X4Job(cfg, store, resolver=fake).run()` on 3 replicates × 2 worlds + 1 N run of tiny synthetic data (M ≈ 20 per panel, 8 panels, d = 8, V = 5): the record has every (space, metric_id) of the SPEC table for views V0–V5; N rows only `x4:<Vk>` S_H1 and `x4:check`; the store gains exactly one artifact (a MetricRecords with config stage `X4`), pre-existing artifacts are byte-identical; parents = union of the runs' parents | contract |
| X10 | Re-running `X4Job.run()` with the same inputs returns the same MetricRecords id and does not raise | contract |
| X11 | A missing run (resolver lists it as missing) gives an `x4` / `run_available` row with status `not_run` and no invented values; the affected verdicts are INCONCLUSIVE | error path |
| X12 | `"X4" in STAGE_REGISTRY` with `requires == ("S4",)` and no gates | contract |
| X13 | `x4_section`: without an X4 record prints "X4: not run"; with one, quotes the prereg `Blinding:` line, the X4-c interpretation line selected by the category and the D-040 addendum verbatim | known answer |
| X14 | `build_e3` from records only: with an empty store prints "not run" for H3 and H4, quotes the prereg H3/H4 rows and D-034 verbatim and writes `condition_P.md`; an S5 verdict REJECTED prints the fixed one-sided reading | known answer |
| X15 | `h4_table` row layout from S6 dynamics rows (t_history, t_rise, class, order null; V1/V5 "not run" without x4curves); `fig_dynamics.png` is written when dynamics rows exist | known answer |
| X16 | `x4_section` under P prints the X4-b note and "decision rule" for H3′, under O neither; `S6Stage.plan` adds `x4curves` when configured and condition P only after an S5 analysis | contract |
| X17 | `"S7" in STAGE_REGISTRY` with `requires == ("S4", "S5")` and `gates == ("G-G",)`; `plan` raises `MISSING_PARENT` on a store without S6 dynamics records; with them, `plan` = `runs_ordered` then the jobs `dev_extract, controls, probes, circular, sensitivity, gate` in that order | contract |
| X18 | `gate_gg` on a memory store: all run records and job records present → `pass`; one planned run without a record → `fail` naming that run; a failed-run record (`outcome: failed`) counts as documented | known answer |
| X19 | `S7Runs.execute` with a training step that raises `StageFailure` (monkeypatch) writes one MetricRecords whose single row is `run_available`, status `not_run`, with the error code in `uncertainty_kind`, and returns its id without raising | error path |
| X20 | `CircularJob.summary` on hand-made rows of 3 panels (one with agreement None): median agreement over the 2 defined panels, `n_panels_above_null_q95` and `n_panels_with_h1_class` hand-counted; `ProbesJob.probe` on planted data (Y = X W + noise, 8 panels): λ chosen on the val panels only (spy), R² > 0.99, shuffled-label rng gives R² < 0.1 | known answer |
| X21 | `s3.on_test_split`: an ActivationSet whose ObservationSet parent has split `dev` is excluded by `activation_ids`; a test-split one is kept | contract |
| X22 | `s8.compare_stores` on two memory stores: identical artifacts → ok, every type counted; a MetricRecords with the same id but a different payload → mismatch named `checksum`; a rerun artifact absent from the main store → `missing`; a `run_timing` record differing only in `wall_time_s` / `tokens_per_second` rows → equal (D-048); GateReports compared by (gate_id, verdict) only | known answer |
| X23 | `s8.integrity`: an intact memory store → ok with n = n_verified; an artifact whose parent id is absent from the store → problem `missing_parent` | error path |
| X24 | `"S8" in STAGE_REGISTRY` with `requires == ("S7",)`, `gates == ("G-H",)`; `RerunJob.run_job` raises `INVALID_CONFIG` when `S3.runs` differs from `S8.rerun_identity_check` | contract |
| X25 | `build_e4` on an empty store writes `summary.md` that prints "not run" for the S7/S8 items and gates G-G/G-H, lists X4-causal and extensions as not run, and invents no number; `probe_table` / `circular_table` / `sensitivity_table` on hand-made rows give hand-computed medians, ranges and counts; a failed control run prints `failed: <reason>` | known answer |
| X26 | X4 Phase B adapter `tests/experiment/test_x4b.py`: two future-map routes agree with the explicit joint and all §3 checks pass; four-state path values; a corrupted marginal is flagged; canonical token inversion (D-019); the read-through store never writes to the main backend; float32 > 1e-4, permutation and float32 status changes are flagged; end-to-end deterministic pool screen with same-symbol partners | known answer + contract |
| X27 | X4 Phase B2 adapter `tests/experiment/test_x4b2.py`: frozen process codes, namespace bits = 5 and disjoint pools; unknown role rejected; deterministic per-role sampling, different streams differ, no states returned; first-token χ² flags bias; chunked beliefs equal unchunked; identical-window counting; ambient link requires the same verdict, spectra and ρ | known answer + contract + error path |
| X28 | circ-audit-v1 `test_circ_audit.py`: C1/C2 per panel with failed baselines excluded and counted; model without an H1 class fails both; three-run reading (all / none / mixed) | known answer |
| X29 | X4-F `test_x4f_probe.py` (independent): nested-ridge isolation, λ tie rule, RidgeProbe equivalence; `test_x4f_gates_smoke.py` (builder): G1–G5 plumbing on a tiny model | contract + smoke |
| X30 | X5 G1 `test_x5g1_lineage.py`, `test_x5g1_controls.py` (independent): named-token remap, paired generators, w33 isolation, permutation equivalence, ledger on every exit, integrity; `test_x5g1_smoke.py` (builder) | contract + smoke |

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

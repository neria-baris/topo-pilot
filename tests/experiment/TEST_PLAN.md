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

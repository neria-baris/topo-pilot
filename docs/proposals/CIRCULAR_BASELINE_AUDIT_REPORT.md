# E4 circular-baseline audit — report

14 October 2026. Protocol [circ-audit-v1](CIRCULAR_BASELINE_AUDIT_PROTOCOL.md), frozen before computation (D-056, commit b9c489d). Branch `e4-circular-audit`. Code: commit e5581e5.

Outputs:
* tables in [CIRCULAR_AUDIT_OUTPUTS/](CIRCULAR_AUDIT_OUTPUTS/): `panels.csv`, `summary.json`, `inputs.json`, `run.json`, `MANIFEST.json`;
* an independent store at `topo-pilot/circular-audit-store/` (MetricRecords `4ddd610fe4684288`, every value `privileged_eval:circular_audit`).

**This is a descriptive audit of already-unblinded E4 data.** It is not independent confirmation. E4, S7 and the B/B2 conclusions are unchanged. **Stopped after the audit.**

## Result

The frozen reading is **BEYOND_SYMBOL_AND_MIXING**.

In all three cylinder-O models, the circular coordinate of resid_post_3 at step 5000 tracks the latent x angle better than two things, in **8/8 panels each (24/24 run-panels)**:

1. **C1:** the in-sample optimistic bound for *any* function of the last symbol.
2. **C2:** the best available last-symbol or mixing baseline (R1, R2, R3, or the b1 circular-mean angle).

| Run (median over 8 panels) | Model A | A*_symbol (optimistic) | Model − A* | Best baseline (median) | Model − best baseline | b32-angle (oracle) | C1 & C2 panels |
|---|---|---|---|---|---|---|---|
| cylinder-O-1729 | 0.891 | 0.817 | +0.072 | b1-angle 0.805 | +0.084 | 0.915 | 8/8 |
| cylinder-O-2718 | 0.892 | 0.817 | +0.071 | b1-angle 0.805 | +0.083 | 0.915 | 8/8 |
| cylinder-O-3141 | 0.884 | 0.817 | +0.066 | b1-angle 0.805 | +0.077 | 0.915 | 8/8 |

* **Margin over the symbol bound:** +0.037 to +0.100 across the 24 run-panels.
* **Margin over the best baseline:** +0.028 to +0.113.
* **Position between symbol and oracle:** the model closes a median of 71% (range 40–91%) of the gap between the symbol-only bound and the exact-belief angle. The belief angle is a reference, not a ceiling for the PH coordinate.
* **Why A*_symbol and the b1/b32 angles repeat across models:** the three models share the same test trajectories and latent angles, and these quantities do not depend on how symbols are relabelled. They are therefore identical across runs, as expected.

## Per model and panel

All PH representations below finished with status `ok`; there was no `no_h1_class` and no estimator failure.

| Seed | Panel | model | R0 | R1 | R2 | R3 | b1-angle | b32-angle | A*_symbol | model − A* | model y-control |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1729 | 1 | 0.892 | 0.059 | 0.770 | 0.699 | 0.190 | 0.804 | 0.921 | 0.818 | +0.073 | 0.110 |
| 1729 | 2 | 0.884 | 0.140 | 0.794 | 0.855 | 0.242 | 0.813 | 0.908 | 0.829 | +0.055 | 0.074 |
| 1729 | 3 | 0.896 | 0.057 | 0.787 | 0.206 | 0.115 | 0.817 | 0.918 | 0.826 | +0.070 | 0.105 |
| 1729 | 4 | 0.903 | 0.018 | 0.766 | 0.191 | 0.267 | 0.790 | 0.913 | 0.804 | +0.100 | 0.081 |
| 1729 | 5 | 0.893 | 0.067 | 0.792 | 0.315 | 0.210 | 0.802 | 0.917 | 0.810 | +0.082 | 0.123 |
| 1729 | 6 | 0.856 | 0.086 | 0.791 | 0.219 | 0.151 | 0.806 | 0.910 | 0.817 | +0.039 | 0.074 |
| 1729 | 7 | 0.891 | 0.040 | 0.798 | 0.072 | 0.066 | 0.805 | 0.923 | 0.816 | +0.075 | 0.139 |
| 1729 | 8 | 0.888 | 0.022 | 0.781 | 0.041 | 0.547 | 0.805 | 0.913 | 0.817 | +0.070 | 0.089 |
| 2718 | 1 | 0.893 | 0.171 | 0.774 | 0.291 | 0.193 | 0.804 | 0.921 | 0.818 | +0.074 | 0.112 |
| 2718 | 2 | 0.885 | 0.201 | 0.785 | 0.857 | 0.086 | 0.813 | 0.908 | 0.829 | +0.056 | 0.083 |
| 2718 | 3 | 0.894 | 0.170 | 0.773 | 0.417 | 0.129 | 0.817 | 0.918 | 0.826 | +0.068 | 0.100 |
| 2718 | 4 | 0.903 | 0.035 | 0.773 | 0.212 | 0.538 | 0.790 | 0.913 | 0.804 | +0.099 | 0.071 |
| 2718 | 5 | 0.892 | 0.072 | 0.756 | 0.271 | 0.217 | 0.802 | 0.917 | 0.810 | +0.081 | 0.127 |
| 2718 | 6 | 0.854 | 0.169 | 0.765 | 0.162 | 0.153 | 0.806 | 0.910 | 0.817 | +0.037 | 0.079 |
| 2718 | 7 | 0.895 | 0.039 | 0.778 | 0.102 | 0.039 | 0.805 | 0.923 | 0.816 | +0.079 | 0.131 |
| 2718 | 8 | 0.883 | 0.047 | 0.783 | 0.042 | 0.547 | 0.805 | 0.913 | 0.817 | +0.065 | 0.080 |
| 3141 | 1 | 0.883 | 0.208 | 0.760 | 0.413 | 0.191 | 0.804 | 0.921 | 0.818 | +0.065 | 0.139 |
| 3141 | 2 | 0.872 | 0.091 | 0.773 | 0.140 | 0.088 | 0.813 | 0.908 | 0.829 | +0.043 | 0.064 |
| 3141 | 3 | 0.885 | 0.130 | 0.776 | 0.197 | 0.198 | 0.817 | 0.918 | 0.826 | +0.059 | 0.126 |
| 3141 | 4 | 0.897 | 0.022 | 0.749 | 0.221 | 0.275 | 0.790 | 0.913 | 0.804 | +0.093 | 0.081 |
| 3141 | 5 | 0.877 | 0.109 | 0.750 | 0.268 | 0.215 | 0.802 | 0.917 | 0.810 | +0.066 | 0.139 |
| 3141 | 6 | 0.869 | 0.046 | 0.771 | 0.171 | 0.152 | 0.806 | 0.910 | 0.817 | +0.052 | 0.085 |
| 3141 | 7 | 0.890 | 0.042 | 0.753 | 0.432 | 0.060 | 0.805 | 0.923 | 0.816 | +0.074 | 0.137 |
| 3141 | 8 | 0.890 | 0.043 | 0.765 | 0.164 | 0.546 | 0.805 | 0.913 | 0.817 | +0.073 | 0.074 |

**R1 (last-symbol embedding).**

* Each panel has 36 distinct points: 476 of the 512 rows are duplicates, because only 36 symbols exist.
* The PH estimator still found an H1 class in every panel. R1's agreement is 0.75–0.80, and every panel is above its permutation null.
* So the trained symbol embedding is itself arranged roughly circularly in x. That is a strong symbol-only explanation, but it stays below A*_symbol (as any last-symbol function must) and below the model.

**R2 / R3 (mixing baselines, existing k = 12).**

* The estimator is unstable across panels: R2 ranges from 0.04 to 0.86, R3 from 0.04 to 0.55.
* R2 has 196–217 distinct points per panel. Its 0.855–0.857 in panel 2 is the only baseline value within 0.03 of the model.
* These are the **existing mixing baselines**, not the best possible two-symbol function. No bound over the last two symbols was frozen or computed.

**Controls.**

* R0 (initialisation) agreement is 0.02–0.21.
* The y-axis (non-periodic) control for the model's coordinate is 0.06–0.14.
* Across the PH representations, y-control agreements range from 0.02 to 0.43.

## Provenance, reproduction and checks

* **Inputs.** All 24 inputs are listed in `inputs.json`, with producer commits and checksums. They were resolved through the S7/S4 resolver, and every cloud and angle used the same history IDs in HistoryIndex order (verified per panel).
* **Symbols and latent angle.** Symbols are each run's own w32; there were 36 distinct symbols in every panel. θ comes from the EvalSidecar, at z32 for each history.
* **Exact reproduction of S7.** All 48 model and R0 run-panels reproduced the stored S7 values exactly: agreement, null q95, p, y-control and b32-angle. This was not a tolerance check.
* **New nulls.** The baselines used new named null streams (`circ_audit_null`).
* **Failures.** None: no estimator failure and no ID mismatch.
* **Main store.** Its listing hash (2,568 files) was identical before and after the run.
* **Cost.** 79.3 CPU-s and 82.1 s wall, against a cap of 3,600 CPU-s. Peak working set 0.41 GB, against an 8 GB target.
* **Tests.**
  - 5 known-answer and property tests for `symbol_only_bound`, including that it dominates every symbol function on both branches and is attained by the group means;
  - 5 tests for the frozen comparison and reading;
  - analysis 138 and experiment 104 passed; ruff, import and file-size checks clean.

## What this licenses — and what it does not

**Can be stated (descriptive, privileged_eval).** In all three cylinder-O models, the leading circular coordinate of resid_post_3 carries x-angle information that no function of the last symbol could reach on the same histories. It also beats the trained last-symbol embedding (R1) and the existing R2/R3 mixing baselines. This closes the specific gap left by E4, which had no direct R1 or symbol-only circular baseline.

**Cannot be stated:**

* That the extra information comes from long or complex history integration. It may come from the last two or three symbols. No bound over two symbols was computed; it was not part of the frozen protocol.
* That the computation uses this coordinate, or that the coordinate is causally relevant.
* That H1 is necessary, or anything about topology beyond a circular coordinate. "Coordinate" here means the estimator's angle.
* Anything held-out or confirmatory. A*_symbol is an in-sample bound. The data were already unblinded. Panels are not replicates; the unit is three training runs of one process.
* Anything about intermediate hooks: only resid_post_3 at p32 was examined.

## Recommendation (one)

**Planning a causal-use test of the coordinate is justified.** This is the frozen protocol's outcome, met in all three runs. The test should be planned, not run: its protocol should be drafted for owner review, with no intervention, extraction or new histories until it is separately approved.

The reasons:

* The symbol-only and mixing explanations do not account for the coordinate. The model beats an *optimistic* last-symbol bound in 24/24 run-panels, by +0.04 to +0.10.
* The audit cannot say *where* the extra information comes from. So the planned test (X4_CAUSAL H4C-F) should include, as frozen controls:
  - a short-context (last-two-symbol) bound or eraser target, alongside the existing R1, local-position and y-axis controls;
  - a held-out check that the coordinate is recoverable at the chosen intermediate hook.

  A causal effect could otherwise reflect immediate-symbol information.

**STOP — owner review. No intervention or further experiment is authorised.**

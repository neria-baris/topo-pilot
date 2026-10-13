# X4-F feasibility gates — report (calibration/validation only)

**Run.** 14 October 2026, handoff job 0003.

**Protocol.** [x4f-exec-v2](X4F_EXECUTION_PROTOCOL_V2.md), frozen by D-061 (sha256 66C9068C…5E45 unchanged).

**Code and run.**

| Item | Value |
|---|---|
| Branch | `x4f-gates` |
| Producer commit | 5c63705 (clean tree) |
| Tables | [X4F_GATES_OUTPUTS/](X4F_GATES_OUTPUTS/) |
| Independent store | `topo-pilot/x4f-gates-research-store/` |
| MetricRecords | `4615fea12afce514` |
| Dev ActivationSets | 4d997fc3837231f4 / 56bf697051eb3794 / 8d8809f4f28b8f12 |

**What did not run.** No fresh trajectory, no test-time or validation ΔR, and no PH check. Main and E4 are unchanged; the main-store listing is identical before and after.

## Verdict: **INCONCLUSIVE** (G4: FAMILY_UNMATCHED in all three models)

| Gate | 1729 | 2718 | 3141 | Note |
|---|---|---|---|---|
| G1 recoverability | PASS | PASS | PASS | m32 R²_val 0.997 / 0.997 / 0.996 (≥ 0.50; shuffled q95 0.039 / 0.022 / 0.035) |
| G2 frozen suffix | PASS | PASS | PASS | identity exact (0 at index 32 and at < 32); primary causality 0; final-null centred Δ 1.2–1.8e-14; weights unchanged |
| G3 erasure | PASS (linear) | PASS | PASS | rank 2; linear R²(h′ → m32) ≈ 0 (≤ 2e-15); label **LINEAR_COMPONENT_ONLY**: RBF R² 0.998 |
| G4 matched family | **INCONCLUSIVE: FAMILY_UNMATCHED** | same | same | 0 of 10,000 draws within 5%; damage profiles not computed |
| G5 support | NOT_RUN | NOT_RUN | NOT_RUN | dependency: G4 did not pass |

Per the frozen rule, the outcome is **not FEASIBLE**. No fresh causal test may be run under x4f-exec-v2. Nothing was retuned, and the site was not changed.

## Details

### G1 (calibration nested selection; one validation score)

| | 1729 | 2718 | 3141 |
|---|---|---|---|
| R²(h → m32) [λ] | 0.9966 [1e-3] | 0.9971 [1e-3] | 0.9961 [1e-3] |
| shuffled q95 (20) | 0.039 | 0.022 | 0.035 |
| trace Var_cal m32 / r2 | 0.844 / 0.060 | 0.844 / 0.059 | 0.844 / 0.060 |
| G1-r2: R²(h → r2) vs q95 | 0.421 vs 0.009 → R2_RECOVERABLE | 0.350 vs 0.004 → R2_RECOVERABLE | 0.358 vs 0.006 → R2_RECOVERABLE |
| (a) direct m2 → m32 | 0.927 | 0.931 | 0.922 |
| (b) affine m2 → m32 | 0.927 | 0.930 | 0.922 |
| (c) affine [m2, h] → m32 | 0.997 | 0.997 | 0.996 |
| direct m1 / affine m1 | 0.772 / 0.772 | 0.792 / 0.791 | 0.769 / 0.769 |
| descriptive: embed / resid_post_3 → m32 | 0.768 / 0.997 | 0.789 / 0.997 | 0.766 / 0.996 |

* The circle expectation is linearly near-perfectly decodable already at resid_post_1.
* The information beyond the last two symbols (r2) is also recoverable there: R² 0.35–0.42, far above its shuffled reference.
* `embed` decodes m32 only about as well as m1, as expected for a last-symbol embedding.

**These are descriptive dev-data results.** They are not a test of causal use.

### G3

* The primary eraser is non-degenerate in every model:
  - k = 128 retained;
  - rank 2, with ρ_max 0.71;
  - idempotence ≤ 1.9e-13;
  - exactness ratio ≤ 1.2e-14.
* After erasure, a linear refit recovers nothing (R² ≈ 0).
* The fixed RBF probe still recovers **R² = 0.998**. The linear eraser therefore removes only the linearly accessible component, and the circle information stays fully available nonlinearly at the same site.
* So even if a matched test had been possible, its result would have been limited to "linearly accessible component" (protocol label, §4/§10).

### G4 — why the random family cannot be matched (descriptive diagnostic)

The frozen run records only the accepted draws, of which there were none. To show the size of the gap, the **same 10,000 seeded draws** were recomputed afterwards (`family_diagnostic.json`, `family_diagnostic_script.py`; 222 CPU s, entered in the ledger). No criterion, fitted object or verdict was changed.

| | 1729 | 2718 | 3141 |
|---|---|---|---|
| primary mean displacement (calibration) | 12.67 | 12.84 | 12.71 |
| random draws: median [q99, max] | 2.01 [3.18, 3.82] | 2.05 [3.25, 4.14] | 2.08 [3.33, 4.26] |
| primary / largest random | 3.3× | 3.1× | 3.0× |
| top-5 eigenvalues of Cov(h) (mean eigenvalue) | 121, 82, 81, 42, 24 (2.97) | 132, 86, 80, 46, 27 (3.14) | 139, 83, 80, 48, 30 (3.21) |

**Interpretation.** m32 is carried by the highest-variance directions of resid_post_1. Random rank-2 subspaces drawn uniformly in the whitened space almost never align with those few directions. The 5% mean-displacement window is therefore unreachable **by construction** for this primary: this is not a sampling shortfall, and more draws would not fix it.

## What can and cannot be concluded

**Can be stated:**

* At resid_post_1, position 32, all three frozen cylinder-O models linearly encode m32 almost perfectly (R² ≈ 0.997).
* They also encode information beyond (w31, w32) (r2, R² 0.35–0.42).
* A rank-2 linear eraser removes the linear component exactly, but leaves the information nonlinearly decodable (RBF R² 0.998).
* The frozen-suffix adapter reproduces the model exactly.

**Cannot be stated:**

* Anything about causal use: no intervention outcome was computed.
* That the coordinate is necessary.
* That the information is long-memory.
* That a different matching rule would succeed. Any change to the random-control construction or the matching rule would be a protocol revision. It needs coordinator review and a new version *before* any further real-data computation.

## Cost, checks and provenance

**Scientific CPU.**

* Gate run: 284.8 CPU s, single-threaded BLAS, peak working set 0.997 GB.
* Diagnostic: 221.7 CPU s.
* **Cumulative X4-F: 506.5 CPU s** of the 10,800 s cap; the first-task cap is 3,600 s.
* Ledger: `cpu_ledger.json` (also in the store).

**Technical CPU (separate).** About 5 minutes of fixture tests and timing probes, not ledgered.

**Tests.**

* learner + analysis + experiment: 438 passed.
* Independent tests (written by a separate agent before it read the implementation), 180 of 181 passing on first contact:
  - `tests/learner/test_patch.py`
  - `tests/analysis/test_x4f_targets.py`
  - `tests/analysis/test_x4f_erasure.py`
  - `tests/analysis/test_x4f_erasure_family.py`
  - `tests/analysis/test_x4f_scores.py`
  - `tests/experiment/test_x4f_probe.py`
* The one first-contact failure was a spec ambiguity in the `knn_ratio` shape; the implementation was aligned with the spec reading.
* Builder smoke test: `test_x4f_gates_smoke.py`.
* ruff, import and file-size checks are clean.

**Inputs.** Frozen IDs were verified: the checkpoints c3358e3c… / 98b0e703… / 036b6707…, the dev HistoryIndexes, the dev ObservationSets, the EmissionSpecs, T and the world, all under the S7 dev-extraction lineage (`inputs.json`). No EvalSidecar was read.

**Alignment.**

* Activation rows match HistoryIndex order and `tokens_hash`.
* Captured and extracted resid_post_1 are identical (difference 0).
* Targets come from public tokens with the oracle kernels, in each model's own vocabulary.

**Exports.** npz files per model (targets, primary map, k) with sha256 hashes in `run.json`.

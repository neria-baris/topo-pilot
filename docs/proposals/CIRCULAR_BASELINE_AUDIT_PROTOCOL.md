# E4 circular-baseline audit — frozen protocol (circ-audit-v1)

**Date and branch.** 14 October 2026, branch `e4-circular-audit` (from 5cd2a49).

**Frozen before any new quantity was computed.** Only the input artifacts' IDs and hooks, and the already-published S7 medians, were inspected.

**Nature of the audit.** It is descriptive and works on existing artifacts only. The data were unblinded in E4. This is not independent confirmation. E4 results and the Phase B/B2 conclusions are unchanged.

## 1. Question

Does the E4 circular result for cylinder O add anything beyond two simpler explanations?

* **Last symbol.** Anything that can be explained by the last symbol alone.
* **Mixing baselines.** The mixing baselines R2 and R3.

The audit does not test causal use, necessity of H1, or complex history integration.

## 2. Inputs (cylinder O, σ 1.25; the S7 panels and histories)

| Seed | ActivationSet step 5000 | ActivationSet step 0 | EvalSidecar (test) | OracleOutputs | HistoryIndex | test ObservationSet | EmissionSpec |
|---|---|---|---|---|---|---|---|
| 1729 | 0e001559534ee7ef | e59d60ad79da2dc9 | f14b01d243a50c1c | efebc05165d4f7bc | afb6e7120c9477b1 | 2a67b2c947e293ba | 3633ac27dab50cf4 |
| 2718 | ec17425cf67f1a54 | 7215d6748ef27d55 | de2bafb822921d67 | d9c6defcc7a9d803 | 908cb61ffbd956c6 | 95c4d118517ecd92 | 97838b9e13a26f74 |
| 3141 | 069da84ce363d8f2 | f2870da82253d42b | 8d1963a30dc6187d | 1731629d61077e96 | 7e7d27bd143ebeb5 | 2e2cf22bb4820155 | 8c29c329c197c79e |

Shared across seeds: WorldSpec 21feee1d8ee5422e and TransitionSpec e4dafc7b9785c172. Reference record: S7 circular a7a60592e32b26fb.

**Resolution.**

* IDs are resolved through the existing S4 `AnalysisJob` resolver, exactly as S7 resolved them. Any mismatch stops the run.
* Panels 1–8 hold 512 histories each, in HistoryIndex order.
* Every cloud must carry the same history IDs in the same order, or the run stops (`SAMPLE_ID_MISMATCH`).
* Symbols are each run's own public tokens w32; no cross-run joins are made.
* No checkpoint is loaded, no activations are extracted, nothing is sampled and nothing is fitted.

## 3. Latent angle and estimator (the S7 procedure, unchanged)

**Latent angles.** These are privileged_eval quantities.

* θ = 2π·x(z32)/12, where z32 comes from the EvalSidecar at end − 1 and x is the periodic axis.
* The control angle θ_y uses the non-periodic y axis (period 12).

**Estimator.**

* Distances: raw Euclidean.
* Coordinates: `CircularCorrespondence(coeff_p = 47, n_perm = 1000).compare`, i.e. the leading H1 cocycle over GF(47) at mid-lifetime.
* Score: agreement A = max(|mean e^{i(φ−θ)}|, |mean e^{i(φ+θ)}|).
* Null: a 1000-permutation null over histories gives q95 and p.

## 4. Representations compared (per run × panel)

| Label | Cloud or angle | Null stream |
|---|---|---|
| model | resid_post_3 at step 5000 (the E4 coordinate) | S7's own `SeedTree(0).generator("circ_null", "cylinder", "O", seed, 5000, panel)` |
| R0 | resid_post_3 at step 0 (existing control) | S7's own stream with step 0 |
| R1 | `SpaceBuilder.baseline("R1")`: `embed` at p32 from the step-5000 set (last-symbol embedding) | `SeedTree(0).generator("circ_audit_null", label, "cylinder", "O", seed, panel)` |
| R2, R3 | `SpaceBuilder.baseline("R2"/"R3")` with the existing k = 12 (`base.yaml`) and no new parameter | same as R1 |
| b1-angle, b32-angle | circular mean of b1, and of b32 (`belief_angle`), with no PH | — |
| y control | the same φ of each PH representation against θ_y | — |

**Reproduction check.** The model and R0 rows must reproduce the stored S7 rows: agreement, null q95, p and control are compared exactly. A mismatch is reported as a provenance failure; values are never silently replaced.

**Per representation and panel, recorded:**

* the status: `ok`, `no_h1_class`, or `estimator_failure` with its error code;
* the number of distinct points and of duplicate rows;
* agreement, null q95, p, and control agreement.

A PH failure on R1 or any other baseline is not proof that the representation lacks angle information.

## 5. Symbol-only optimistic bound (privileged_eval)

Per panel:

  A*_symbol = (1/M) Σ_w |Σ_{i: w32_i = w} exp(iθ_i)|.

**Property.** Every angle that is a function of the last symbol alone has agreement ≤ A*_symbol with θ on the same histories. Both the rotation and the reflection branch are covered.

**Labelling.** It is computed in-sample from latent θ and labelled an **in-sample optimistic bound**, not a held-out predictor. Latent data are used only in this evaluation.

## 6. Frozen descriptive comparison and reading

For each run r and panel i, two conditions:

* **C1:** A_model > A*_symbol.
* **C2:** A_model > the maximum of the available agreements among {R1, R2, R3, b1-angle}. A baseline whose status is not `ok` is left out of the maximum and counted.

A run **adds beyond symbol and mixing** if C1 and C2 both hold in at least 7 of 8 panels (the project's usual panel rule).

| Runs meeting the rule | Reading | Recommendation |
|---|---|---|
| All 3 | The circular coordinate carries x-angle information beyond any last-symbol function and the mixing baselines (descriptive) | Planning a coordinate causal-use test is justified. Planning only: intervention needs separate approval. |
| 0 | The symbol/mixing explanation is not excluded and suffices for now | Do not plan a causal-use test on this basis. |
| 1–2 | Mixed | Treat as not established; no causal-test planning. |

**Also reported, not decisive:**

* the margins A_model − A*_symbol and A_model − max(baselines), as medians and ranges over panels;
* panels above the null q95;
* the R0 and y-axis controls;
* b32-angle as the oracle reference.

Panels and pairs are not replicates. The unit is the training run; there are no p-values over panels.

## 7. Code, budget and outputs

**Code.**

* One pure function, `analysis.symbol_only_bound`, with known-answer tests.
* One orchestration module, `experiment/circ_audit.py`.
* Reused unchanged: `CircularCorrespondence`, `CircularCoordinates`, `SpaceBuilder` and the S7 resolver.

**Budget.** At most 1 CPU hour of process time; 8 GB RAM target, measured as peak working set. Exceeding the cap means stop.

**Main store.** Read-only. Its listing hash must be equal before and after the run.

**Outputs.**

* An independent store `topo-pilot/circular-audit-store/` holding one MetricRecords. Every value is labelled `privileged_eval:circular_audit`.
* Tables in `docs/proposals/CIRCULAR_AUDIT_OUTPUTS/`.
* The report `docs/proposals/CIRCULAR_BASELINE_AUDIT_REPORT.md`.

**Prohibited.**

* No sampling, training, decoder, extraction or intervention.
* No change to E4, S7, B/B2, earlier decisions, main or tags.
* No merge or push.

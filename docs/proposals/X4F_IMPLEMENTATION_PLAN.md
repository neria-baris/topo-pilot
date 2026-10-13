# X4-F implementation plan (for the draft protocol x4f-draft-1)

14 October 2026. Branch `x4f-planning`. **Plan only.** Nothing described here has been implemented or run. It implements [X4F_COORDINATE_CAUSAL_PROTOCOL_DRAFT.md](X4F_COORDINATE_CAUSAL_PROTOCOL_DRAFT.md) once the owner approves it. Scope follows [RESEARCH_HARNESS_ARCHITECTURE.md](RESEARCH_HARNESS_ARCHITECTURE.md): M8 (frozen intervention), plus small M4 and M6 pieces. Excluded:

* native Q2 and p31 branches;
* X5 and X6;
* any general learner, oracle, intervention or scheduler framework.

## 1. Existing code that is reused unchanged

| Need | Existing component |
|---|---|
| Frozen model | `learner.load_model(Checkpoint)`: eval mode, CPU. `TransformerLM` has `tok_emb`, `pos_emb`, `blocks[0..3]`, `ln_final` and `unembed`. |
| Dev histories | S7 dev HistoryIndexes `d9fe461a56797514` / `880c3e8ec8347b72` / `d5e64c5398ef4c25`, panels 1–8 |
| Extraction | `activations.ActivationStage.run(checkpoint, obs, index, hooks, panels, store)`. The S7 dev sets hold resid_post_3 only, so resid_post_1 needs a **new extraction (owner decision 3)**. |
| Oracle targets | `oracle.BayesFilter` gives b32, and b2 from the two-token history. `LastSymbolPosterior` gives b1. `FutureOperator.F1` gives Q1. |
| Probes | `prediction.RidgeProbe`, with the S7 probe protocol for λ and standardisation |
| Fresh lineage | the pattern of `experiment/x4b2.py`: `HMMSampler` on E_canon, a frozen named stream, a new namespace, states discarded. For X4-F the canonical tokens are mapped through each model's `symbol_perm`. |
| PH check | `analysis.CircularCorrespondence` (the S7 estimator) |
| Provenance | `ReadThroughBackend`, `listing_hash`, `Budget` and `peak_memory_bytes` (fixed in 741333c), `provenance_row`, MetricRecords |

## 2. Minimal frozen-forward adapter (M8): new, learner-side

**Why in learner.** It runs the model, which only `learner`/`activations` may do. It receives public tokens and a precomputed numeric replacement. It never sees targets, beliefs, the oracle, analysis code or sidecars, so the access and import policies are preserved.

```python
def resume_from_site(model: TransformerLM, inputs: LongTensor[R, 33], site: str,
                     position: int, replacement: Tensor[R, d]) -> Tensor[R, V]:
    """Logits at `position` after replacing that position's vector at `site`.
    site ∈ {"resid_post_k" (k < n_layers - 1), "ln_final_out"}.
    resid_post_k: embed → blocks[0..k] → x[:, position] = replacement → blocks[k+1..] →
    ln_final → unembed. ln_final_out: normal forward to ln_final, replace the normed vector,
    unembed directly (no second LayerNorm). Model stays in eval, no grad, weights untouched."""
```

* **Where the transform is built.** The experiment module builds the replacement from the stored or captured vector using analysis-fitted numeric maps. The learner never knows what a transform means.
* **Capture.** Existing `forward(return_hooks=...)` provides the unpatched vectors, so no new capture API is needed.
* **Errors:** `UNKNOWN_HOOK` for a bad site, `ALIGNMENT_ERROR` for a shape or position mismatch, `NUMERICAL_FAILURE` for non-finite input.
* **Tests** (independent test writer, tiny 2-layer fixture model; no real artifacts):
  - **Identity:** replacement = the captured vector reproduces the logits of `forward` within 1e-6.
  - **Causality:** patching position p leaves the logits at positions < p unchanged (verified on the full-sequence variant).
  - **Final-null:** at ln_final_out, adding a vector in the null space of the centred readout leaves the centred logits unchanged within 1e-8 (float64 copy).
  - **Effect:** a non-identity patch changes position-p logits.
  - **Weights:** they are bitwise identical before and after.
  - **Error paths:** each error code above.
  - **Imports:** `tools/check_imports.py` confirms that learner still imports no world, process, oracle, analysis or prediction code.

## 3. New pure analysis functions (analysis part g; no I/O)

| Function | Math | Known-answer tests |
|---|---|---|
| `circle_expectation(b, x_coords, period)` | m = Σ_z b_z (cos, sin)(2π x_z / period) | a delta belief gives a unit vector; a uniform-x belief gives 0 |
| `fit_linear_eraser(X, Z)` | oblique LEACE for continuous Z: whitening W = Σ_xx^{-1/2}; P = projection onto the column space of W Σ_xz; x′ = x − W⁺ P W (x − μ). Returns μ, the map, the rank and the norm. | after erasure the calibration cross-covariance with Z is 0 within 1e-10; a planted 2-D target is erased; rank ≤ dim Z |
| `random_matched_erasers(X, rank, target_disp, n, rng, tol=0.05, max_draws)` | random rank-r subspaces in whitened space, accepted iff the mean displacement is within 5% | acceptance rule on synthetic data; reports failure when no match is possible |
| `support_diagnostics(X_cal, X_patched)` | Ledoit–Wolf Mahalanobis distance, fraction beyond the calibration q99, kNN ratio | the identity patch gives about 1% beyond q99; a large shift is flagged |
| `regret_delta(Q1, p, p_I)` | per-history KL difference in nats | hand values; 0 for the identity |
| `paired_bootstrap_canonical(values_by_model, keys, n, rng)` | joint resampling of canonical keys across models | deterministic draws; a constant input gives a zero-width CI |

The existing `RidgeProbe` covers G1, G3 and the readout refit. The RBF random-feature residual probe is a fixed-seed feature map followed by `RidgeProbe`; it is added as a 20-line helper with a test.

## 4. Orchestration (experiment; not a registered stage, no stages.yaml change)

| Step | Module | Output |
|---|---|---|
| F1 targets | `x4f_targets.py`: b32, b2, b1 and Q1 from the oracle kernels on dev and test tokens; m32, m2, m1, r2; the local-position and y targets | per-history target export (npz + sha256) |
| F2 extraction | via `ActivationStage` (owner decision 3) | new dev ActivationSets with hooks resid_post_1, resid_post_3 and embed, in the **independent store**. The main store stays read-only and its listing hash is checked. |
| F3 gates | `x4f_gates.py`: G1–G5 on calibration/validation; erasers and controls fitted and frozen | gate report + frozen transform export (μ, maps, ranks, norms, accepted random seeds); **STOP** |
| F4 fresh lineage | `x4f_lineage.py`: stream `SeedTree(0).generator("x4f-v1", "test", "cylinder", "overlap", "1.25")`, namespace code 6, 4,096 canonical trajectories mapped to each model's vocabulary | tokens export; canonical key → history-ID map per model |
| F5 causal test | `x4f_run.py`: identity check, then every frozen intervention through `resume_from_site`; ΔR, the bootstrap and the H4C-F verdict | MetricRecords + per-history regret/displacement export; **STOP** |

**Provenance in every output.** Each output records:

* the protocol document sha256 and the producer commit;
* checkpoint IDs and ActivationSet IDs;
* the T/E/π IDs, and the canonical maps and symbol_perms;
* the named seeds: `x4f-v1/random_eraser/<model>/<k>`, `x4f-v1/shuffle/<model>`, `x4f-v1/bootstrap`;
* the transform checksums, and the gate verdicts with their reasons.

**Exports are not frozen core types.** Per-history arrays are versioned npz exports with checksums, and aggregates are MetricRecords. No core contract changes.

## 5. Cost estimate (unbenchmarked planning figures)

| Item | Estimate |
|---|---|
| Dev extraction (3 models × 4,096 histories × 33 positions, forward only) | < 1 CPU min |
| Eraser and probe fitting (128-dim, 3,072 rows; ridge λ grid; RBF 2,048 features) | a few CPU min |
| Random-eraser matching (up to 10,000 draws per model) | < 1 CPU min |
| Gate interventions on validation (about 30 interventions × 1,024 histories × 3 models; suffix of 2 blocks) | about 5 CPU min |
| Fresh-test interventions (about 120 incl. dose curves × 4,096 × 3; about 1 s each from about 60k tokens/s forward, derived from the S3 training throughput) | 10–20 CPU min |
| Bootstrap (2,000 draws × controls) and PH check (2 panels × 3 models × 2) | < 5 CPU min |
| **Total** | about 0.5–1 CPU h; **proposed cap 3 CPU h**, 8 GB RAM, ≤ 300 MB outputs (logits kept only for identity and primary) |
| Engineering | about 2–3 working days: adapter + independent tests 0.5 d; analysis functions + tests 1 d; gates orchestration 0.5 d; lineage and run 0.5 d; report 0.5 d |

## 6. Testing and review discipline

* **Independent tests.** `learner` (adapter) and `analysis` (erasers, decision helpers) get tests written independently of the implementation, from this plan and the protocol (ORCHESTRATOR §2).
* **Test scope.** Module suites only, after each change (`tools/affected_tests.py`). The integration suite is not required for planning-stage code.
* **Real-data dry runs.** No real-data dry run of interventions on the test pool, ever. Development uses fixtures; gates use calibration/validation only.

## 7. Limitations known in advance

* **Linear erasure.** It may leave nonlinearly accessible circle information, which G3 reports. A null may mean redundancy or downstream recomputation; a positive concerns only the erased linear component.
* **Off-manifold hybrids.** Erased and donor vectors can be off-manifold (G5). Rank and displacement matching does not equalise predictive damage, so damage profiles are reported for every control.
* **What the evidence can show.** Three models of one process; a sign-level p of 0.125 at best. No population, LLM or topology-necessity claim.
* **Target origin.** m32 is a belief expectation, so effects attributed to it can come from local-position information. The local-position and generic-predictive controls address this only partly.
* **Short-context control.** It uses the stationary prior and two symbols. Information beyond two symbols is not long memory.
* **resid_post_1 is untested.** The site was chosen from X4_CAUSAL, not from data. If G1 fails there, the protocol stops. Choosing another site would require a new protocol, not a substitution.

## 8. Explicitly not planned now

Native Q2 or p31 continuation; a topology-altering (type C) manipulation; Fisher pullback diagnostics; X5/X6; Phase C; any new world, oracle, learner abstraction, scheduler or schema change; training.

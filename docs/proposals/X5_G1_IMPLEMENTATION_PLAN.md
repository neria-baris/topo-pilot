# X5 G1 — implementation plan (for x5g1-feas-draft-1) and prospective training outline

14 October 2026. Handoff job 0004. **Plan only.** Nothing is implemented, sampled or trained.

**Scope.**

* Sections 1–5 cover the oracle and kernel feasibility gate of [X5_G1_FEASIBILITY_PROTOCOL_DRAFT.md](X5_G1_FEASIBILITY_PROTOCOL_DRAFT.md).
* Section 6 is a **training outline for later review**. It is not a frozen protocol.

**Out of scope.** No universal harness, no registries and no contract changes, except the small additions listed in §1, which are flagged for review.

## 1. Smallest adapters

| Where | Addition | Why it cannot be avoided | Review flag |
|---|---|---|---|
| process (new file `conductance.py`; exported) | `ConductanceConfig(a: float = 0.20, move: float = 0.8)`, plus the pure functions `warp_profile(dims, a) -> (f[y], l_h[y])` and `conductance_kernel(world, cfg) -> (TransitionSpec, metadata)` | `TransitionBuilder` implements only `max_degree_lazy_walk`; its `TransitionConfig.kind` is a `Literal` and should not be widened silently | new public process API, **for review** |
| process `ProcessStage` | `run_conductance_transition(world_id, cfg, store) -> id`. It saves the TransitionSpec with config {kind: "metric_conductance", a, move, f_y, l_h, C_max, edge_count_h, edge_count_v} and the parent WorldSpec. | keeps "process touches the store only in its Stage" (CONVENTIONS §3) | small extension of an existing class, **for review** |
| analysis (new file `x5_kernel.py`) | pure diagnostics: `movement_rate`, `spectrum_report` (λ, gap, γ*, t_rel, mixing bound), `integrated_autocorrelation(T, pi, g)`, `rate_matched_kernel(T, alpha)` with its status, `is_connected(T)` | does not exist yet | none (array-only kernels) |
| experiment (new `x5g1_*.py`) | input resolution and integrity; the calibration lineage adapter (reusing the x4b2 pattern: `HMMSampler`, frozen stream, namespace code 8, states discarded); oracle quantities via `BayesFilter`, `LastSymbolPosterior`, `context_gain`, `FutureOperator`; the G_C bootstrap; the verdict; exports; the ledger (`try/finally`); STOP and budget polling inside loops | orchestration only | none |
| contracts, world, dataset, oracle, learner | **no change** | — | — |

**Explicitly not built:**

* a new WorldSpec or metric literal;
* a generalized non-symmetric kernel contract;
* a G2 emission builder, or density / initial-law adapters;
* PH runs (deferred);
* any trainer change. Training adapters are §6 and later.

## 2. Pure functions: definitions the tests will target

* **`warp_profile(dims=(12, 12), a)`.**
  - f(y) = (12/2π)·(1 + a·cos(2πy/11)) and l_h(y) = 1 + a·cos(2πy/11), for y = 0..11.
  - |a| ≥ 1 → `INVALID_CONFIG` (that would make f ≤ 0).
* **`conductance_kernel(world, cfg)`.**
  - Classify each edge as horizontal or vertical by coordinates; assert 144 / 132 edges; otherwise `STATE_ORDER_MISMATCH`.
  - c = 1/l²; C_max = max row sum; T_ij = move·c_ij/C_max for i ≠ j; T_ii = 1 − row sum.
  - Call `check_support` and `TransitionSpec.validate()`.
  - Errors: `NONSTOCHASTIC`, `STATIONARITY_FAILURE`, `INVALID_CONFIG`.
* **`integrated_autocorrelation(T, pi, g)`.**
  - Eigendecompose the symmetric T (uniform π).
  - w_k = ⟨g − ḡ, φ_k⟩²_π, and τ = Σ_{k≥2} w_k(1 + λ_k)/(1 − λ_k) / Σ_{k≥2} w_k.
  - A constant g gives the status `UNDEFINED_CONSTANT`.
  - λ_k = 1 for some k ≥ 2 (reducible) gives the status `REDUCIBLE`.
* **`rate_matched_kernel(T, alpha)`.**
  - Returns I + α(T − I) with status ok, or `INVALID_KERNEL` if α ≤ 0, any entry < 0, or the diagonal is < 0.2 − 1e-12.

## 3. Independent tests

As in X4-F, a separate test-writer agent writes them from the protocol and §2, before reading the implementation. Fixtures are synthetic only.

| Module | Required cases |
|---|---|
| process | a = 0 reproduces `TransitionBuilder(max_degree_lazy_walk, 0.2)` on the 12×12 cylinder within 1e-15; a = 0.2 is symmetric, stochastic, lazy (≥ 0.2), edge-supported, connected and uniform-stationary; a hand value of C_max on the full 12×12 cylinder from the closed form, max_y (2/l_h(y)² + n_vert(y)) with n_vert = 2 for interior rows and 1 for boundary rows; horizontal/vertical classification including wrap edges; \|a\| ≥ 1 error; metadata arrays equal to `warp_profile` |
| analysis | τ_int on a 2-state lazy chain (hand value); a constant g gives `UNDEFINED_CONSTANT`; a reducible block-diagonal T gives `REDUCIBLE`; spectral gap and t_rel hand values; the mixing bound formula; `rate_matched_kernel` validity boundary and invalid cases; connectivity of a disconnected fixture |
| experiment (builder smoke) | the lineage adapter's frozen seeds and namespaces; paired common randomness (same z1 and first symbol across arms on a tiny HMM); states never returned; the ledger is written when an exception is raised mid-run (`try/finally`); STOP raised inside the bootstrap loop |

## 4. Execution sequence (a later job, after ACCEPT of the protocol)

1. Freeze the protocol (DECISIONS) and commit the code and tests. Producer commit = clean tree.
2. Run the integrity check: parents, checksums, state and edge order, the main-store listing hash.
3. Build both kernels, run the a0 equivalence check, validity checks and diagnostics. This is exact and needs no data.
4. Draw the calibration pools: arm a0 first, then a020, with the same stream and distinct namespaces. Run the disjointness checks.
5. Compute the oracle quantities per pool in 4,096-row batches, then the G_C bootstrap, polling STOP and budget throughout.
6. Write the verdict, exports and ledger; STOP for review.

## 5. Cost

| Item | Estimate |
|---|---|
| Kernels and diagnostics | seconds |
| Sampling, 2 × 16,384 × 33 | under 1 CPU min |
| Filters, 2 × 16,384 × 32 × 144 | about 1 CPU min |
| Bootstrap, 2 × 2,000 row-mean resamples | seconds |
| **Expected total** | **≤ 0.1 CPU h** (cap 1 CPU h; X5 cumulative 6 CPU h) |
| Storage | ≤ 50 MB (tokens + beliefs npz) |
| Engineering | about 1.5 days, including the independent tests |

## 6. Prospective training outline (NOT frozen; for a later reviewed protocol)

### 6.1 Design

Two kernels (a0, a020) × **three new paired masters**. The originals 1729/2718/3141 are anchors only, not paired controls.

| Item | Proposed |
|---|---|
| Fixed between arms | the current architecture and optimizer (base.yaml); 131,072 training histories per arm; batch 128; 5,000 updates; O emissions σ 1.25; the E payload and symbol naming |
| Paired within a master (where lawful) | initial weights; batch-index order; the dataset uniform streams (initial state, emissions, transitions) |

### 6.2 Endpoint (unchanged rules)

* **τ.** The first evaluation step at which regret/G_C ≤ 0.05 on the fixed per-arm dev set, sustained over three consecutive evaluations (the crossing plus the next two).
  - Regret is the mean over dev histories of KL(q_C ‖ p_model) at p32.
  - G_C comes from the arm's frozen calibration pool.
* **Practical delay.** At least 250 steps, unchanged.
* **Decision rule.** Supported if every uncensored pair has τ_a020 − τ_a0 ≥ 250, with a positive paired-resampling difference. Rejected if any pair's upper bound is < 250. Otherwise inconclusive.

### 6.3 Ambiguities to resolve before any training protocol is frozen, with proposed resolutions

1. **Evaluation grid and censoring.**
   * **Ambiguity.** The grid is every 100 steps to 1,000, then every 250 to 5,000 (29 points). τ is interval-censored to (previous grid point, crossing], and a crossing at 4,750 or 5,000 lacks two confirmations.
   * **Proposal.** Report τ as an interval. Treat τ as right-censored if confirmations are missing, and never substitute 5,000. Base the decision on the interval endpoints: with the paired difference defined from intervals, "≥ 250" requires the lower difference bound τ_a020,low − τ_a0,high ≥ 250.
2. **Dev-trajectory bootstrap.**
   * **Ambiguity.** τ is a functional of a whole regret curve, and the arms have different dev sets.
   * **Proposal.** Draw a per-arm dev set of 4,096 under paired common randomness, indexed by the same index i. Resample the index set i jointly (2,000 draws), recompute both regret curves and τ, and take a percentile interval for the paired difference.
3. **Threshold evidence.** A grid-resolution difference of a few points could straddle 250. **Proposal:** use the conservative interval rule in 1; ties count as not ≥ 250.
4. **Target-token alignment and exposure.** Training loss covers all 33 positions, but regret is measured at p32 only.
   * **Proposal:** report exposure as steps × 128 × 33 target tokens (≈ 21.1 M at 5,000) and unique training histories (131,072).
   * Report position-wise regret at the final checkpoint as descriptive.
5. **Initial-weight and batch pairing.**
   * **Ambiguity.** The trainer seeds init and batch order from `run_key = (world, condition, seed)`. Identical keys pair the arms but collide in checkpoint identity; distinct keys break the pairing.
   * **Proposal:** a small reviewed adapter that passes an explicit **pairing key**, (x5g1, master), for init and batch order, while the run identity includes the arm.
6. **Dataset lineage collisions.**
   * **Ambiguity.** `DatasetStage` scopes its streams and sequence-ID process codes by (family, mode, σ, master), so both arms would get **identical sequence IDs**. Worse, its world-scoped test stream (`SeedTree(0)`) would make the a0 arm **reproduce the original, unblinded test set**.
   * **Proposal:** a reviewed dataset lineage adapter that keeps the same uniform streams for pairing but adds the arm and the namespace "x5g1-v1" to the sequence-ID code. Train, dev and fresh test each get new named streams; the fresh test is never the original one.
7. **Final fresh test.** Use 4,096 new trajectories per arm (paired common randomness, new namespace), evaluated once at step 5,000. Secondary outcomes: final regret (nats), normalized regret and AUC.
8. **Checkpoints and storage.**
   * 29 evaluations × 6 models × about 3.3 MB ≈ 0.6 GB if every evaluation checkpoint is kept.
   * **Proposal:** evaluate regret on the fly at the grid points, and keep only the checkpoints at steps 0, 100, 500, 1,000 and 5,000 (≈ 0.1 GB) for the descriptive geometry.
   * This fits within 2 GB.
9. **Compute.** About 13–16 CPU min per model from E2/E3, plus about 29 dev evaluations per model. Estimate 2–3 CPU h for six models, within the X5 6 CPU h cap (shared with this gate).

**Training cannot start on the gate contract.** It needs ACCEPT of a separate training protocol, which resolves 1–8, and a distinct task.

## 7. Risks

* **Weak context.** G_C may be < 0.03 for one arm. That stops the comparison; a is not retuned.
* **Rate confound.** C_max normalisation is expected to lower the curved arm's movement rate (not yet computed), so any learning-time difference is confounded with speed and mixing. The rate-matched kernel is only a diagnostic here.
* **Low power.** Three pairs give weak power; a sign-level result is the best case.

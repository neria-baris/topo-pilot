# X5 G1 — exact-process and calibration feasibility protocol (x5g1-feas-v2)

14 October 2026. Handoff job 0005. Branch `x5-g1-planning`, from bf5073e.

**Status.** Prepared for coordinator review. It freezes only on ACCEPT, before any real computation. Nothing has been computed, sampled, implemented or trained.

**Relation to other documents.**

* It supersedes [x5g1-feas-draft-1](X5_G1_FEASIBILITY_PROTOCOL_DRAFT.md), which is kept byte-identical. §10 lists every change.
* Basis: [X5_GEOMETRY_OPTIMIZATION.md](X5_GEOMETRY_OPTIMIZATION.md).
* Training is out of scope here; see [X5_G1_IMPLEMENTATION_PLAN_V2.md](X5_G1_IMPLEMENTATION_PLAN_V2.md) §6, which is NOT frozen.

**Choices adopted from the review of job 0004:**

* 16,384 trajectories per arm;
* the 95%-bound G_C rule, with the 0.03 nat threshold unchanged;
* a single original E payload;
* the IAT function set;
* PH deferred;
* the small conductance and ProcessStage APIs, with no schema change.

## 1. Question and claims boundary

Do both lawful processes provide enough history-dependent next-symbol information for a later learning-time comparison to be meaningful? The two processes share the same 144-state cylinder and the same E: the flat max-degree walk a0, and the metric-coupled conductance walk a020.

These are process-level statements only. Even matching summaries would license no curvature-specific attribution.

## 2. Frozen inputs and objects

| Object | ID / value |
|---|---|
| WorldSpec | `21feee1d8ee5422e` (cylinder 12×12, flat metric literal unchanged; no new WorldSpec) |
| TransitionSpec a0 | `e4dafc7b9785c172` (max_degree_lazy_walk, p_stay 0.2, uniform π), reused |
| EmissionSpec | `3633ac27dab50cf4` (overlap, σ 1.25, replicate 1729): **the stored numeric E and its stored `symbol_perm`, unchanged**, for both arms |

**State order (assertion failure → FAILED: STATE_ORDER).**

* State id = x·12 + y.
* Horizontal edges are those whose endpoints share y: 144, including 12 wraps.
* Vertical edges are those whose endpoints share x: 132.

**Arm a020 kernel.**

* f(y) = (12/2π)(1 + 0.20·cos(2πy/11)), and the horizontal length is l_h(y) = 1 + 0.20·cos(2πy/11). Vertical edges have length 1.
* Conductances: c = 1/l² on edges.
* C_max = max_i Σ_j c_ij.
* T_ij = 0.8·c_ij/C_max for i ≠ j, and T_ii = 1 − Σ_{j≠i} T_ij.
* **a0 equivalence:** the same builder at a = 0 must reproduce `e4dafc7b9785c172` within 1e-15, else FAILED: A0_EQUIVALENCE.
* **Storage:** the existing `TransitionSpec` schema (π uniform, p_stay 0.2, d_max 4), with f, l_h, c, C_max and a in the artifact config. It is saved in the independent store with the WorldSpec as parent.
* **G0:** metadata only, an analytic identity. No sampling or training.

**Privileges.**

| Data | Class |
|---|---|
| T, E, π, kernel metadata, beliefs, predictive laws, G_C | oracle / analysis |
| Named tokens and sequence IDs | public |
| Latent states | discarded right after the sampler's range check; never persisted or passed on; no EvalSidecar written |

## 3. Kernel validity and exact process diagnostics

### 3.1 Validity per arm

Any failure gives `INVALID_KERNEL` for that arm.

| Property | Condition |
|---|---|
| Rows | sum to 1 within 1e-12 |
| Entries | ≥ 0 |
| Symmetry | max \|T − Tᵀ\| ≤ 1e-12 |
| Laziness | min T_ii ≥ 0.2 − 1e-12 |
| Support | edges and the diagonal only |
| Stationarity | \|πT − π\|∞ ≤ 1e-12 |
| Connectedness | the positive off-diagonal graph has one component |
| Symbols | p_w = πE ≥ 1e-4 for every w |

### 3.2 Diagnostics (descriptive; exact)

* **Movement rate:** r = Σ_z π_z(1 − T_zz).
* **Spectrum.** All eigenvalues, the gap 1 − λ₂, the absolute gap γ* = 1 − max(|λ₂|, |λ_min|), and t_rel = 1/γ*.
* **Mixing upper bound (discrete time):**

  t_mix(ε) ≤ ⌈ t_rel · log(1/(ε·π_min)) ⌉ steps, with ε = 1/4 and π_min = 1/144.

  Assumptions: the chain is irreducible, reversible with respect to π (T is symmetric with uniform π), and aperiodic (lazy). This is a bound, not an estimate.
* **Status for γ\* ≤ 1e-12:**
  - `NEAR_UNIT_GAP` if the connectivity check passed: the diagnostic is reported as numerical failure, and the arm is INCONCLUSIVE.
  - `REDUCIBLE` if connectivity failed, which already makes the kernel INVALID_KERNEL.
* **Integrated autocorrelation of conditional-state functions** (exact spectral form).
  - With orthonormal φ_k under π, w_k = ⟨g − π(g), φ_k⟩²_π and τ_int(g) = Σ_{k≥2} w_k(1 + λ_k)/(1 − λ_k) / Σ_{k≥2} w_k.
  - **Fixed functions g:** cos(2πx/12), sin(2πx/12), the centred y, and g_w(z) = E[z, w], **the conditional emission probability as a state function**, for each of the 36 w. For g_w, the mean, minimum and maximum are reported.
  - These are **state-process diagnostics**. They are not autocorrelations of the observed token sequence, whose lag-0 term contains emission noise.
  - Statuses: `UNDEFINED_CONSTANT` if Var_π(g) ≤ 1e-12, and `REDUCIBLE` if λ_k ≥ 1 − 1e-12 for some k ≥ 2.
* **Rate-matched flat kernel (process diagnostic only).**
  - α = r_a020 / r_a0 and T_α = I + α(T_a0 − I).
  - It is valid iff α > 0, every entry is ≥ 0, and the minimum diagonal is ≥ 0.2 − 1e-12; otherwise `INVALID_KERNEL` for this diagnostic.
  - Its validity or values **never affect the gate verdict**.
  - Attached statement: a scalar α cannot match a spectrum, and matching summaries leaves anisotropy, entropy, context gain and the full correlations as alternatives.

## 4. Calibration pools, sampling and naming

**Paired common randomness.** Each arm gets its **own, separately initialised** generator from the **same** seed:

```text
rng_a0   = SeedTree(0).generator("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")
rng_a020 = SeedTree(0).generator("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")
```

* These are two independent objects with identical seed and state. An advanced generator is never reused across arms.
* SeedTree master: 0 (frozen).
* Each arm is drawn with **one** call, `HMMSampler(T_arm, E[:, perm], π, SequenceLayout()).sample(16_384, rng_arm)`. The sampler consumes uniforms in the same order (z1, then per step emission and transition), so trajectory i in both arms shares z1 and the first canonical symbol.
* No batching of the sampling call, because batching would change the uniform order.

**Naming.**

* `canon` = the sampler's tokens (canonical indices), and **named = perm[canon]**, with perm the stored `symbol_perm` of `3633ac27dab50cf4`. This is the D-019 convention, identical to `DatasetStage._sample_all`.
* All persisted public tokens and **all oracle calls use the named tokens with the stored E**. Canonical tokens are never persisted and never passed to the oracle.

**Persistence.**

* Each pool is an `ObservationSet` with `split = "dev"` (an existing schema literal), V = 36, and named tokens.
* Artifact config: {role: "calibration", protocol: "x5g1-feas-v2", arm, stream, namespace_code: 8}.
* Parents: [the arm's TransitionSpec, EmissionSpec `3633ac27dab50cf4`].
* It is saved in the independent store `topo-pilot/x5g1-research-store/`.
* Resolvers must select by role and protocol, **never** by split alone.

**Sequence IDs.** `(process_code("cylinder", "overlap", "1.25", "x5g1-v1:calibration:" + arm) << 32) | (8 << 28) | index`.

* Code 8 is independent of the schema split and unused elsewhere (DatasetStage uses 1–3, x4b2 5, x4f 6).
* **Disjointness** (failure → FAILED): from every stored ObservationSet, from the B2 and X4-F namespaces, and between arms. Identical windows with old data are reported only.

**Other rules.**

* Latents are discarded.
* No retries or enlargement.
* The pool size of 16,384 per arm is frozen.

**Future-token isolation.** Oracle quantities at p32 use only w1..w32. The 33rd token is stored as public data but is read by no gate quantity. A test checks that changing w33 leaves every gate quantity unchanged.

## 5. Context and information quantities (per arm; float64; oracle batch 4,096 rows)

| Quantity | Definition | Role |
|---|---|---|
| **G_C** (repository, D-020) | mean_h KL(q_C(h) ‖ q_last(h)) in nats, with q_C = b32·T·E and q_last = r_{w32}·T·E (π prior); `oracle.context_gain`. Equals H(W33 \| W32) − H(W33 \| W1..32). | **gate** |
| G_C interval | bootstrap over pool rows: 2,000 draws; stream `SeedTree(0).generator("x5g1-v1", "gc_bootstrap", arm)`; each draw is `rng.integers(0, 16384, 16384)`, in 4 batches of 500 draws; percentile interval `np.quantile(·, [0.025, 0.975], method="linear")` | gate status |
| Paired G_C difference | resample indices shared across arms (stream "gc_bootstrap_paired"), same method | **descriptive only** |
| Stationary-marginal G_C | mean KL(q_C ‖ πE) | descriptive |
| H(W\|Z), H(W) | from E and π (identical across arms) | descriptive |
| Bayes entropy by position t = 0..32 | mean_h H(q_t) | descriptive |
| Two-token comparator | mean KL(q_C ‖ b2·T·E), with b2 the posterior on (w31, w32) under π | descriptive |
| Observability | singular values of O1 and O2 (`observability_matrices(2)`) | descriptive |

**No division by G_C occurs in this gate.**

**Per-arm context status.** Exact comparisons use float64.

| Status | Condition |
|---|---|
| **INVALID_PREDICTIVE** | any non-finite value, a predictive row that fails its sum or nonnegativity check, or a KL that is undefined (zero predictive mass where the other law is positive). Numerical, not weak. |
| **PASS** | finite interval with lower bound ≥ 0.03 (equality passes) |
| **FAIL** (weak context) | finite interval with upper bound < 0.03. This includes a valid G_C of exactly 0 or any small finite value. |
| **NEAR_THRESHOLD** | otherwise (lower < 0.03 ≤ upper) |

## 6. PH — deferred

PH does not enter the feasibility decision, so it is deferred. If ever run, it is descriptive only.

## 7. Execution controls

* **Budget.** ≤ 1 CPU h for this gate, charged to the X5 cumulative 6 CPU h; 8 GB; ≤ 2 GB storage. Expected ≤ 0.1 CPU h.
* **Polling.** STOP and budget are checked **before and after** every operation: integrity, each kernel, each diagnostic block, each sampling call, each 4,096-row oracle batch, each 500-draw bootstrap batch, and each export.
* **X5 ledger.**
  - Written in `try/finally`. It records CPU on success, failure, STOP and budget exhaustion, **including export cost**.
  - It is never reset. Nothing is retried.
* **Integrity.** Parent payload checksums and the main-store listing hash are checked before and after. A mismatch gives **FAILED**, and the run is invalid as a scientific result.
* **Reproducibility.** The protocol hash and producer commit (clean tree) are recorded. Exports are immutable, with checksums.

## 8. Verdict and precedence (frozen)

Per arm, operational status:

* FAILED (integrity, state order, a0 equivalence, namespace collision);
* INVALID_KERNEL;
* NEAR_UNIT_GAP;
* or ok.

Per arm, context status: PASS, FAIL, NEAR_THRESHOLD or INVALID_PREDICTIVE.

**Overall verdict, by precedence** (the first matching row wins, so a weak arm can never conceal an invalid one):

1. **FAILED.** Any FAILED condition in any arm or globally.
2. **INCONCLUSIVE.** Any arm with INVALID_KERNEL or NEAR_UNIT_GAP, any arm INVALID_PREDICTIVE or NEAR_THRESHOLD, budget exhaustion, or STOP.
3. **WEAK_CONTEXT.** Any arm FAIL, with every other arm PASS or FAIL. This is a scoped stop for this process pair, horizon and position; a is not retuned.
4. **FEASIBLE.** Both arms valid, ok and PASS.

The rate-matched α diagnostic never enters this table.

**Effect.** FEASIBLE authorises only proposing a training protocol. Training cannot start on this contract.

## 9. Frozen parameters

| Parameter | Value |
|---|---|
| Arms | a0 (`e4dafc7b9785c172`), a020 (as §2) |
| E | `3633ac27dab50cf4` (numeric E and symbol_perm unchanged); named = perm[canon] |
| Pool | 16,384 per arm; one sampling call per arm; separately initialised generators from SeedTree(0) stream ("x5g1-v1", "calibration", "cylinder", "overlap", "1.25") |
| Persistence | ObservationSet split "dev", role "calibration"; ID namespace code 8 |
| G_C gate | 0.03 nat; PASS lower ≥ 0.03; FAIL upper < 0.03; else NEAR_THRESHOLD; INVALID_PREDICTIVE only for numerical invalidity |
| Bootstrap | 2,000 draws; 4 × 500; stream ("x5g1-v1", "gc_bootstrap", arm); percentile, linear |
| Oracle batch | 4,096 rows |
| Mixing | ε = 1/4, π_min = 1/144, ⌈·⌉ |
| Tolerances | kernel 1e-12; a0 1e-15; variance/gap floors 1e-12 |
| Budget | gate ≤ 1 CPU h; X5 ≤ 6 CPU h; 8 GB; ≤ 2 GB storage |

## 10. Changes from draft-1 (before any data)

| # | Draft-1 | v2 | Review item |
|---|---|---|---|
| 1 | Sampling and oracle in canonical order | named = perm[canon]; persisted tokens and oracle calls use named tokens with the stored E; non-identity-permutation equivalence and round-trip tests; w33 isolation | 1 |
| 2 | "Same stream feeds both arms" | two separately initialised generators with identical seed; one sampling call per arm; master 0 frozen; bootstrap naming and quantile method frozen; paired bootstrap descriptive only | 2 |
| 3 | G_C ≤ 1e-6 → undefined | a valid weak G_C (including 0) is FAIL; only numerical invalidity is INVALID_PREDICTIVE; equality at 0.03 defined; explicit precedence FAILED > INCONCLUSIVE > WEAK_CONTEXT > FEASIBLE; no division by G_C | 3 |
| 4 | pools exported as npz (implicit) | ObservationSet split "dev", role "calibration"; namespace code 8 independent of the split | 4 |
| 5 | mixing bound without ceil; IAT labels; STOP after operations only | ⌈·⌉; conditional-state IAT labels; constant, reducible and near-unit statuses; STOP and budget before and after every operation; `try/finally` ledger with failure and export cost; integrity failure invalidates the run | 5 |

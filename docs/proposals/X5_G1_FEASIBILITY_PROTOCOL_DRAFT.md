# X5 G1 — exact-process and calibration feasibility protocol (x5g1-feas-draft-1)

14 October 2026. Handoff job 0004. Branch `x5-g1-planning`, from 10ed372.

**Draft for coordinator review.** It freezes only on ACCEPT, before any real computation. Nothing here has been computed, sampled or trained.

* **Basis:** [X5_GEOMETRY_OPTIMIZATION.md](X5_GEOMETRY_OPTIMIZATION.md) (G0/G1/G2 and Stage 0), and [RESEARCH_HARNESS_ARCHITECTURE.md](RESEARCH_HARNESS_ARCHITECTURE.md) (case C).
* **Scope of this protocol:** the oracle and kernel feasibility gate for G1 **only**.
* **Not covered:** training. The training outline is in [X5_G1_IMPLEMENTATION_PLAN.md](X5_G1_IMPLEMENTATION_PLAN.md) §6. Training needs a separately reviewed protocol and task.

## 1. Question and claims boundary

Do the two specified stochastic processes provide enough history-dependent next-symbol information for a later learning-time comparison to be meaningful? Both use the same 144-state cylinder and the same emissions: one has the flat max-degree walk (a = 0) and one the metric-coupled conductance walk (a = 0.20). The gate also has to confirm that both kernels are lawful.

The gate concerns two **defined processes**. Even if their mixing summaries matched, nothing here licenses curvature-specific attribution. Geometry summaries are not a causal curvature test.

## 2. Frozen inputs and objects

### 2.1 Parents (from immutable metadata; verified at run start; mismatch → FAILED)

| Object | ID | Role |
|---|---|---|
| WorldSpec | `21feee1d8ee5422e` (cylinder, dims 12×12, flat metric) | the complex: states, edges, coords. Unchanged and **never re-labelled with a curved metric**. |
| TransitionSpec, flat | `e4dafc7b9785c172` (max_degree_lazy_walk, p_stay 0.2, uniform π) | arm **a0** (reused as stored) |
| EmissionSpec | `3633ac27dab50cf4` (overlap, σ 1.25, replicate 1729) | the **single E payload** for both arms. Its symbol_perm is kept. Sampling uses E_canon = E[:, symbol_perm], which is identical across the three O replicates (D-052 check). |

**State, coordinate and edge order.**

* State id = x·12 + y, with coords[:, 0] = x (periodic) and coords[:, 1] = y (0..11).
* An edge is *horizontal* iff its endpoints share y. Those 144 edges include the 12 wrap edges (x = 0 ↔ x = 11).
* An edge is *vertical* iff its endpoints share x; there are 132.
* The run asserts these counts and the absence of any other edge. Any deviation gives `FAILED: STATE_ORDER`.

### 2.2 Arm a020: the metric-coupled conductance kernel

* **Warp profile.** R = 12/(2π) and f(y) = R·[1 + 0.20·cos(2πy/11)], for y = 0..11.
* **Edge lengths.**
  - horizontal edges at row y: l_h(y) = f(y)·2π/12 = 1 + 0.20·cos(2πy/11);
  - vertical edges: 1.
* **Conductances.** c_ij = 1/l_ij² on edges, and 0 elsewhere.
* **Kernel.** C_max = max_i Σ_j c_ij. Then T_ij = 0.8·c_ij/C_max for i ≠ j, and T_ii = 1 − Σ_{j≠i} T_ij.
* **Equivalence check (G0/a0).** The same formula with a = 0 must reproduce the stored flat T `e4dafc7b9785c172` with max |Δ| ≤ 1e-15. Otherwise `FAILED: A0_EQUIVALENCE`.
* **Metadata, not a forged metric.** f(y), l_h(y), every c_ij, C_max and a are stored as **explicit artifact-config metadata** of the new TransitionSpec, plus a checksummed npz export. The WorldSpec metric literal stays "flat"; no new WorldSpec is made.
* **Schema.** The new kernel uses the existing `TransitionSpec` schema: T, π = 1/144, p_stay = 0.2 (the lazy floor guaranteed by the 0.8 factor), d_max = 4 (the graph's maximum degree, unchanged) and event_order.
* **Lineage.** Its parent is the WorldSpec, and it is saved in the independent X5 store (§7).

### 2.3 G0 (metadata-only)

Attaching a metric to the same complex with unchanged numeric T, E and initial law leaves the token law identical by construction. G0 needs no sampling and no duplicate training. It is recorded as the analytic statement plus the a0 equivalence check above.

### 2.4 Privileges

| Data | Class | Readers |
|---|---|---|
| T, E, π, f, l, c, C_max, kernel diagnostics | process/oracle-only | experiment, analysis, oracle |
| calibration tokens and sequence IDs | public | any |
| latent states from the sampler | **discarded at once**; never persisted or passed on | none |
| beliefs, predictive laws, GC, regrets | oracle/analysis | experiment, analysis |

The learner is not involved in this gate.

## 3. Kernel validity and process diagnostics (exact; no sampling)

### 3.1 Validity (per arm; any failure → arm status `INVALID_KERNEL`)

| Property | Condition |
|---|---|
| Stochasticity | rows sum to 1 within 1e-12 |
| Nonnegativity | min T ≥ 0 |
| Symmetry | max \|T − Tᵀ\| ≤ 1e-12 |
| Laziness | min T_ii ≥ 0.2 − 1e-12 |
| Support | edges and the diagonal only |
| Stationarity | \|πT − π\|∞ ≤ 1e-12, with π uniform |
| Connectedness | the graph of positive off-diagonal entries has one component (irreducible). Laziness gives aperiodicity. |
| Symbol probabilities | p_w = πE ≥ 1e-4 for every w (the same E in both arms) |

### 3.2 Diagnostics (descriptive unless stated; exact linear algebra)

* **Movement rate:** r = Σ_z π_z (1 − T_zz).
* **Spectrum.** All eigenvalues of the symmetric T, in descending order, with:
  - the spectral gap 1 − λ₂;
  - the absolute gap γ* = 1 − max(|λ₂|, |λ_min|);
  - the relaxation time t_rel = 1/γ*.
* **Mixing bound.** t_mix(ε) ≤ t_rel · log(1/(ε·π_min)), with ε = 1/4 and π_min = 1/144. This is the standard bound for reversible chains. Assumptions: a reversible (symmetric) chain with uniform π; the bound is an upper bound, not an estimate.
* **Integrated autocorrelation** of fixed state functions g, exact for this reversible chain from the eigen-decomposition T = Σ_k λ_k φ_k φ_kᵀ (orthonormal under π):
  - ρ_g(t) = Σ_{k≥2} λ_k^t w_k / Σ_{k≥2} w_k, with w_k = ⟨g − π(g), φ_k⟩_π²;
  - τ_int(g) = Σ_{k≥2} w_k (1 + λ_k)/(1 − λ_k) / Σ_{k≥2} w_k.
* **Functions g, fixed in advance:**
  - cos(2πx/12) and sin(2πx/12);
  - the centred y;
  - the symbol-probability functions g_w(z) = E[z, w] for each of the 36 symbols. For these, the mean, minimum and maximum of τ_int over w are reported.
* **Rate-matched flat kernel (process diagnostic only, never a training arm).**
  - α = r_a020 / r_a0 and T_flat,α = I + α(T_a0 − I).
  - It is valid iff α > 0, its minimum entry is ≥ 0, and its minimum diagonal is ≥ 0.2 − 1e-12. Otherwise the status is `INVALID_KERNEL` for this diagnostic, which does not affect the G1 verdict.
  - Reported: its rate (equal to r_a020 by construction), gap, t_rel and τ_int, and their differences from the a020 kernel.
* **Statement attached to every summary.** A scalar α cannot match a whole spectrum, and matching any of these summaries leaves anisotropy, entropy, context gain and the full correlations as alternative explanations.

## 4. Calibration pools (one fixed pool per arm)

| Item | Frozen value |
|---|---|
| Size | 16,384 trajectories per arm; 33 symbols each; history = w1..w32; target position p32 |
| Sampler | `dataset.HMMSampler(T_arm, E_canon, π, SequenceLayout())`, which draws z1 ~ π, emits, then transitions (D-019 canonical order) |
| Stream (**paired common randomness**) | `SeedTree(0).generator("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")`. The **same** stream feeds both arms, so trajectory i in each arm consumes identical uniforms in identical order. Its z1 and first symbol are identical across arms; later paths differ because T differs. |
| Sequence-ID namespace | `(process_code("cylinder", "overlap", "1.25", "x5g1-v1:calibration:" + arm) << 32) \| (8 << 28) \| index`, with arm ∈ {a0, a020}. Code 8 is unused by DatasetStage (1/2/3), x4b2 (5) and x4f (6, reserved). |
| Disjointness checks (failure → FAILED) | sequence IDs disjoint from every stored ObservationSet, from the B2 and X4-F namespaces, and between arms. Identical 32-symbol windows with old data are reported, not an error. |
| Latents | discarded immediately after the sampler's range check |
| Retries / enlargement | none; a weak result is never resampled |

Later dev, train and test data for training get their own namespaces (plan §6) and are never drawn from this stream.

## 5. Context and information quantities (per arm, on its calibration pool; float64 oracle kernels)

| Quantity | Definition | Role |
|---|---|---|
| **G_C** (repository definition, D-020) | mean over pool histories of KL(q_C(h) ‖ q_last(h)) in nats. q_C = b32·T·E is the full-history Bayes predictive at p32; q_last = r_{w32}·T·E is the last-symbol posterior under π (`oracle.context_gain`). This equals E[H(W33 \| W32)] − E[H(W33 \| W1..32)] under the process law. | **Gate** |
| G_C uncertainty | trajectory bootstrap, 2,000 draws, stream ("x5g1-v1", "gc_bootstrap", arm); 95% percentile interval | gate status rule |
| G_C-stationary (comparison only) | mean KL(q_C ‖ πE): full history against the stationary symbol marginal | descriptive |
| H(W\|Z), H(W) | from E and π, in nats (identical across arms by construction) | descriptive |
| Bayes entropy by position | for t = 0..32, the mean over pool histories of the entropy H(q_t) in nats (`BayesFilter` q) | descriptive |
| Two-token comparator regret | mean KL(q_C ‖ q_2), with q_2 = b2·T·E and b2 the posterior from (w31, w32) under π | descriptive |
| Observability | singular values of O1 and O2 from `FutureOperator.observability_matrices(2)` (horizon 3 is not built) | descriptive |

**G_C gate (per arm; threshold 0.03 nats, unchanged from X5).**

| Status | Condition |
|---|---|
| PASS | the 95% lower bound is ≥ 0.03 |
| FAIL (weak context) | the 95% upper bound is < 0.03 |
| NEAR_THRESHOLD | the interval contains 0.03; this is INCONCLUSIVE |
| GC_UNDEFINED | G_C ≤ 1e-6 or non-finite; this is INCONCLUSIVE |

No other pass threshold is introduced. In particular, nothing is borrowed from the completed X4 results.

## 6. PH and geometry — deferred

World, emission, belief and future PH would not change the training-feasibility decision, which depends only on kernel validity and G_C. They are therefore **deferred**. If ever run, they are descriptive only; geometry summaries are not a causal curvature test.

## 7. Execution, budget and provenance

**Budget.**

* X5 total: ≤ 6 CPU h, 8 GB RAM, ≤ 2 GB added storage.
* This gate: ≤ 1 CPU h, charged to that cumulative X5 budget. Expected well under 0.1 CPU h: two 16,384-trajectory pools, 144×144 spectra, and a 2,000-draw bootstrap of row means.
* Technical fixture tests are reported separately.

**Controls inside the run.**

* STOP and budget are checked after each pool, after each oracle batch of 4,096 rows, every 500 bootstrap draws, and after each diagnostic block.
* An **X5 ledger** (separate from the X4 ledger) is written in `try/finally`, so a failure or cancellation still records CPU used.
* The ledger is never reset, and nothing is retried silently.

**Integrity.**

* The main-store listing hash is checked before and after the run, and the parent payload checksums are verified.
* Any mismatch gives **FAILED**. That is not a scientific verdict.

**Provenance.**

* Source code is frozen (committed, clean tree) before any data.
* Independent store: `topo-pilot/x5g1-research-store/`.
* Every output records the protocol hash, producer commit, parents, streams, namespaces, the kernel metadata and npz checksums.

## 8. Gate verdict (frozen)

| Verdict | Condition |
|---|---|
| **FEASIBLE** | both arms are valid kernels (§3.1), the a0 equivalence holds, and G_C PASS in both arms |
| **WEAK_CONTEXT** (scoped stop) | both kernels are valid and some arm's G_C is FAIL. It applies to this process pair, horizon and position only. No retuning of a. |
| **INCONCLUSIVE** | NEAR_THRESHOLD, GC_UNDEFINED, `INVALID_KERNEL` in a G1 arm, a numerical failure, or the budget cap reached |
| **FAILED** | source or parent integrity mismatch, state-order or a0-equivalence failure, or a namespace collision |

FEASIBLE authorises **only** proposing a training protocol. No training starts on this gate contract.

## 9. Open choices for coordinator review

1. **Pool size.** 16,384 per arm is proposed; with a bootstrap interval the gate is decided by the interval, not by n.
2. **Near-threshold handling.** Lower bound ≥ 0.03 for PASS is proposed, rather than the point estimate.
3. **Single E payload.** Replicate 1729's EmissionSpec, in canonical sampling order. The symbol naming of later training masters is decided in the training protocol.
4. **τ_int functions.** cos/sin of x, y and the 36 g_w. Add or remove any before freeze.
